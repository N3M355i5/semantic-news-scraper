import time
import random
from urllib import response

import requests
import feedparser

from config.settings import RSS_TIMEOUT
from rss.rss_parser import RSSParser


class RSSClient:

    BASE_URL = "https://news.google.com/rss/search"

    def __init__(self):

        self.parser = RSSParser()

    ##############################################################

    def search(self, query: str):

        params = {

            "q": query,

            "hl": "en-US",

            "gl": "US",

            "ceid": "US:en"

        }

        response = requests.get(

            self.BASE_URL,

            params=params,

            timeout=RSS_TIMEOUT,

            headers={

                "User-Agent":
                "Mozilla/5.0"

            }

        )

        ##############################################################
        # Google rate limit
        ##############################################################

        if response.status_code == 503:

            raise RuntimeError("GOOGLE_RATE_LIMIT")

        print(response.status_code)

        print(response.url)

        print(response.text[:1000])

        feed = feedparser.parse(

            response.text

        )

        print("Feed Entries:", len(feed.entries))

        return self.parser.parse(feed)