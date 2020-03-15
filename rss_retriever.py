import json
import sys
import collections

import feedparser
import requests

def feed_saver(rss_urls_filename: str, storage_filename: str):
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
                news_data.update(feed_retriever(req_url.text))
        
        if news_data:
            with open(storage_filename, "w") as f:
                json.dump(news_data, f, indent=4)


def feed_retriever(file: str):
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
            # try updating the feed_data dict with rss dict retrieved in feed["items"]
            feed_data[feed["channel"]["title"]].append({
                    "title": item["title"], 
                    "published": item["published"],
                    "link": item["link"], 
                    "summary": item["summary"]
                })
        except:
            # sometimes this happens when a rss feed lacks of some required entries
            print("ERROR:", sys.exc_info())
            if item["link"]:
                print("ERROR FEED LINK:", item["link"])

    return feed_data


if __name__ == "__main__":
    feed_saver("rss_urls.json", "feed_data.json")