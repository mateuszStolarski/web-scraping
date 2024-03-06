from mongo_scrapper.items.base import BaseItem


class TwitterItem(BaseItem):
    date: str
    from_search: bool
