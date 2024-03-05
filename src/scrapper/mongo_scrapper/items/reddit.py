from mongo_scrapper.items.base import BaseItem


class RedditItem(BaseItem):
    subreddit: str
