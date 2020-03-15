import collections
import json
import pathlib
import sys

import feedparser
import requests

import nlp


class RSSRetriever:
    def __init__(self):
        self.nlp = nlp.NLP()

    def feed_saver(self, rss_urls_filename: str, storage_filename: str, keywords: set = {}):
        """ Given a json file containing news rss urls stores the feeds into another json file.
        
        Args:
            rss_urls_filename (str): filename of the json file containing news rss urls.
            storage_filename (str): filename of the json file that stores the retrieved data.
            keywords (set, optional): a set of keywords strings in the feeds to look for. Defaults to {}.
        """
        with open(rss_urls_filename, "r") as f:
            urls = json.load(f)
            with open(storage_filename, "r") as f:
                news_data = json.load(f)
                for url in urls:
                    # Checks if the url response is 200(OK) and assign requests.get(url) to req_url
                    if (req_url := requests.get(url)).status_code == 200:
                        news_data.update(self.feed_retriever(req_url.text, keywords))
        
        if news_data:
            with open(storage_filename, "w") as f:
                json.dump(news_data, f, indent=4)


    def feed_retriever(self, file: str, keywords: set = {}):
        """ Given a news rss file returns a dictionary of news data.
        
        Args:
            file (str): news rss file.
            keywords (set, optional): a set of keywords strings in the feeds to look for. Defaults to {}.
        
        Returns:
            dict: returns a dictionary of the news data.
            
        """
        feed = feedparser.parse(file)
        feed_data = collections.defaultdict(list)
        for item in feed["items"]:
            try:
                # True if there are no keywords found in both the title and the summary
                if not self.check_keywords(item["title"], keywords)  \
                    and not self.check_keywords(item["summary"], keywords):
                    continue

                sentiment = self.nlp.analyze(item["summary"])
                # Tries updating the feed_data dict with rss dict retrieved in feed["items"]
                feed_data[item["link"]] = {
                        "category": feed["channel"]["title"],
                        "title": item["title"],
                        "published": item["published"],
                        "summary": item["summary"],
                        "summary_sentiment_score": sentiment["score"],
                        "summary_sentiment_magnitude": sentiment["magnitude"]
                    }
            except:
                # Sometimes this happens when a rss feed lacks of some required entries
                error_message = f"ERROR: {sys.exc_info()[:2]}"
                if item["link"]:
                    error_message = error_message + ", " + item["link"]
                # print(error_message)

        return feed_data


    def check_keywords(self, text: str, keywords: set = {}):
        """ Checks if the text contains any keyword in the set.
        
        Args:
            text (str): text to be analyzed.
            keywords (set, optional): a set of keywords strings in the feeds to look for. Defaults to {}.
        
        Returns:
            bool: True if no keywords are provided or the text contains any keyword in the set.
        """
        # If no keywords, return True
        if not keywords:
            return True

        # Creates a string with only alphabets and spaces
        cleantext = "".join([letter.lower() for letter in text if letter.isalpha() or letter == " "])
        # Split the string by the spaces
        cleantextlist = cleantext.split()
        lower_keywords = {keyword.lower() for keyword in keywords}
        for word in cleantextlist:
            if word in lower_keywords:
                return True
        return False


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.resolve()
    rss_retriever = RSSRetriever()
    rss_retriever.feed_saver(f"{path}/rss_urls.json", f"{path}/feed_data.json", {"Coronavirus"})