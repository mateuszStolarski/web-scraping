import json
import time
from typing import Iterable

from bs4 import BeautifulSoup
from mongo_scrapper.items.base import BaseItem
from mongo_scrapper.items.twitter import TwitterItem
from mongo_scrapper.spider_settings.twitter import TwitterSettings
from mongo_scrapper.spiders.base import BaseSpider
from scrapy.http import JsonRequest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

SCROLL_PAUSE_TIME = 0.5


class TwitterSpider(BaseSpider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    start_urls = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        self._twitter_settings = TwitterSettings()

        self.start_urls = [
            f"https://twitter.com/{user}" for user in self._twitter_settings.profiles
        ]
        self.start_urls.extend(
            [
                f"https://twitter.com/search?q=#{tag}&src=recent_search_click"
                for tag in self._twitter_settings.hastags
            ]
        )

    def start_requests(self):
        option = webdriver.ChromeOptions()

        option.add_argument("--headless")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        option.experimental_options["prefs"] = chrome_prefs
        option.enable_downloads = True
        driver = webdriver.Remote(
            "http://selenium:4444/wd/hub",
            DesiredCapabilities.CHROME,
            options=option,
        )
        driver.maximize_window()
        driver.get(url)
        time.sleep(2)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll = True
        tries = 0

        while scroll:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            tries += 1
            tweet_texts = soup.find_all("div", {"data-testid": "tweetText"})
            if tries == 50 or len(tweet_texts):
                scroll = False

        resp = driver.page_source
        driver.close()
        soup = BeautifulSoup(resp, "html.parser")
        for url in self.start_urls:
            try:
                # options = webdriver.ChromeOptions()
                # options.add_argument("--no-sandbox")
                # options.add_argument("--window-size=1920,1080")
                # options.add_argument("--headless")
                # options.add_argument("--disable-gpu")
                # driver = webdriver.Remote(
                #     "http://localhost:4444/wd/hub",
                #     DesiredCapabilities.CHROME,
                #     options=options,
                # )

                tweet_texts = soup.find_all("div", {"data-testid": "tweetText"})
                replies = soup.find_all("div", {"data-testid": "reply"})
                likes = soup.find_all("div", {"data-testid": "like"})
                user_names = soup.find_all("div", {"data-testid": "User-Name"})

                yield JsonRequest(
                    url="https://httpbin.org/status/200",
                    data={
                        "tweet_texts": [tweet_text.text for tweet_text in tweet_texts],
                        "replies": [reply.text for reply in replies],
                        "likes": [like.text for like in likes],
                        "user_names": [user_name.text for user_name in user_names],
                        "target_url": url,
                    },
                    callback=self.parse,
                )
            except:
                continue

    def parse(self, response) -> Iterable[BaseItem]:
        body = json.loads(response.request.body)

        for user_names, tweet_texts, replies, likes in zip(
            body["user_names"],
            body["tweet_texts"],
            body["replies"],
            body["likes"],
            strict=True,
        ):
            yield TwitterItem(
                index=user_names,
                user=user_names.split("·")[0],
                text=tweet_texts,
                number_of_comments=int(replies),
                likes=int(likes),
                date=user_names.split("·")[1],
                from_search=bool("https://twitter.com/search?q=" in body["target_url"]),
            )
