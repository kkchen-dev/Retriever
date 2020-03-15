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

    def feed_saver(self, rss_urls_filename: str, storage_filename: str):
        """ Given a json file containing news rss urls store the feeds into another json file
        
        Args:
            rss_urls_filename (str): filename of the json file containing news rss urls
            storage_filename (str): filename of the json file that stores the retrieved data
        """
        with open(rss_urls_filename, "r") as f:
            urls = json.load(f)
            news_data = {}
            with open(storage_filename, "r") as f:
                news_data = json.load(f)
            
            for url in urls:
                # check if the url response is 200(OK) and assign requests.get(url) to req_url
                if (req_url := requests.get(url)).status_code == 200:
                    news_data.update(self.feed_retriever(req_url.text))
        
        if news_data:
            with open(storage_filename, "w") as f:
                json.dump(news_data, f, indent=4)


    def feed_retriever(self, file: str):
        """ Given a news rss file returns a dictionary of news data.
        
        Args:
            file (str): news rss file
        
        Returns:
            dict: dictionary of news data:

            {source:list({"title": str, "published": str, "link": str,"summary": str})}
        """
        feed = feedparser.parse(file)
        feed_data = collections.defaultdict(list)
        for item in feed["items"]:
            try:
                sentiment = self.nlp.analyze(item["summary"])
                # try updating the feed_data dict with rss dict retrieved in feed["items"]
                feed_data[feed["channel"]["title"]].append({
                        "title": item["title"],
                        "published": item["published"],
                        "link": item["link"],
                        "summary": item["summary"],
                        "summary_sentiment_score": sentiment["score"],
                        "summary_sentiment_magnitude": sentiment["magnitude"]
                        
                    })
            except:
                # sometimes this happens when a rss feed lacks of some required entries
                error_message = f"ERROR: {sys.exc_info()[:2]}"
                if item["link"]:
                    error_message = error_message + ", " + item["link"]
                print(error_message)

        return feed_data


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.resolve()
    rss_retriever = RSSRetriever()
    rss_retriever.feed_saver(f"{path}/rss_urls.json", f"{path}/feed_data.json")