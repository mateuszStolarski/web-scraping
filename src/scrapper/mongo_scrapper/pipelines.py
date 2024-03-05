import sys

from mongo_scrapper.db.mongo import MongoDataBase
from mongo_scrapper.items.base import BaseItem
from mongo_scrapper.spider_settings.mongo import MongoSettings
from mongo_scrapper.spiders.base import BaseSpider
from scrapy import Spider


class MongoScrapperPipeline:
    def __init__(self) -> None:
        settings = MongoSettings()
        if not settings.connection_string:
            sys.exit("You need to provide a Connection String.")
        self._db = MongoDataBase(settings.connection_string)

    def open_spider(self, spider: BaseSpider) -> None:
        spider.collection = self._db.get_collection(spider.name)

    def close_spider(self, spider: Spider) -> None:
        self._db.client.close()

    def process_item(
        self,
        item: BaseItem,
        spider: BaseSpider,
    ) -> BaseItem:
        spider.collection.update_one(
            filter={
                "index": item.index,
            },
            update={
                "$setOnInsert": dict(item),
            },
            upsert=True,
        )

        return item
