from scrapy.spiders import CrawlSpider


class TwitterSpider(CrawlSpider):
    name = "twitter"
    allowed_domains = ["twitter.com"]

    def parse(self, response):
        pass
