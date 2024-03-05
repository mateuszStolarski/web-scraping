from pymongo.collection import Collection
from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):
    name = "base"
    _collection: Collection = None

    @property
    def collection(self) -> Collection:
        return self._collection

    @collection.setter
    def collection(self, value: Collection) -> None:
        self._collection = value
