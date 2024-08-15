import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/"]

    def parse(self, response):
        pass
