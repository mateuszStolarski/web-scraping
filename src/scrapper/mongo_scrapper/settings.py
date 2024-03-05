BOT_NAME = "mongo_scrapper"

SPIDER_MODULES = ["mongo_scrapper.spiders"]
NEWSPIDER_MODULE = "mongo_scrapper.spiders"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "mongo_scrapper.pipelines.MongoScrapperPipeline": 300,
}
