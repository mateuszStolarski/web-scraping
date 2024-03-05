from mongo_scrapper.items.base import BaseItem


class TwitterItem(BaseItem):
    profile: str
    is_popular: bool
