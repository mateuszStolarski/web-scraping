from typing import Iterable

from mongo_scrapper.items.base import BaseItem
from mongo_scrapper.items.reddit import RedditItem
from mongo_scrapper.spider_settings.reddit import RedditSettings
from mongo_scrapper.spiders.base import BaseSpider
from scrapy import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class RedditSpider(BaseSpider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = [
        f"http://www.reddit.com/r/{subreddit}/new"
        for subreddit in RedditSettings().subreddits
    ]

    rules = [
        Rule(
            LinkExtractor(allow=[f"/r/{subreddit}/new"]),
            callback="parse_item",
        )
        for subreddit in RedditSettings().subreddits
    ]
    _counter = 0  # counter for returned posts
    _scroll_base = "https://www.reddit.com/svc/shreddit/community-more-posts/new"

    def parse_item(self, response: HtmlResponse) -> Iterable[BaseItem]:
        selector_list = response.css("shreddit-post")
        for selector in selector_list:
            subreddit = selector.attrib["subreddit-prefixed-name"]

            if (
                selector.css("svg.hidden.stickied-status") and self._counter <= 100
            ):  # exclude pinned posts
                self._counter += 1
                yield RedditItem(
                    index=selector.attrib["id"],
                    subreddit=selector.attrib["subreddit-prefixed-name"],
                    user=selector.attrib["author"],
                    text=selector.attrib["post-title"],
                    number_of_comments=selector.attrib["comment-count"],
                    likes=selector.attrib["score"],
                )

        if self._counter <= 100 and selector_list:
            # load more posts
            more_post_cursor = selector.attrib["more-posts-cursor"]
            feed_index = selector.attrib["feedindex"]
            subreddit = subreddit[2:]
            url = f"{self._scroll_base}/?after={more_post_cursor.encode()}&t=DAY&name={subreddit}&feedLength={feed_index}&adDistance=2"
            yield Request(url, callback=self.parse_item)
