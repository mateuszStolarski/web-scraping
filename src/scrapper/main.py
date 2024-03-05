import logging
import time

from mongo_scrapper import settings
from mongo_scrapper.spider_settings.base import ScrapperSettings
from mongo_scrapper.spiders.reddit import RedditSpider
from mongo_scrapper.spiders.twitter import TwitterSpider
from scrapy.crawler import CrawlerProcess


def crawl(process: CrawlerProcess, settings: ScrapperSettings) -> None:
    process.start(stop_after_crawl=not settings.run_every_hour)
    while settings.run_every_hour:
        time.sleep(3600)
        process.start(stop_after_crawl=not settings.run_every_hour)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    env_settings = ScrapperSettings()
    logging.info(f"Running every hour: {env_settings.run_every_hour}")

    process = CrawlerProcess(settings=settings.__dict__)
    process.crawl(TwitterSpider)
    process.crawl(RedditSpider)

    crawl(
        process=process,
        settings=env_settings,
    )


if __name__ == "__main__":
    main()
