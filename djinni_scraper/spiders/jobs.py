import random
import time

import scrapy
from scrapy.http import Response


class VacanciesSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["djinni.co"]
    start_urls = ["https://djinni.co/jobs/?primary_keyword=Python"]
    download_delay = 3
    job_links = set()

    def parse(self, response: Response, **kwargs) -> None:
        job_links = response.css("ul.list-unstyled.list-jobs.mb-4 a::attr(href)").getall()
        for job_link in job_links:
            if job_link not in self.job_links:
                self.job_links.add(job_link)
                yield response.follow(job_link, callback=self.parse_job)

    @staticmethod
    def parse_job(response: Response) -> None:
        time.sleep(random.uniform(1, 3))

        job_title = response.css(
            "body > div.wrapper > div.page-content > div > header > div.detail--title-wrapper > div > div > h1::text"
        ).get().strip()

        job_technologies = response.css(
            "body > div.wrapper > div.page-content > div > div:nth-child(2) > div.col-sm-4.row-mobile-order-1 > "
            "aside > div > ul:nth-child(3) > li:nth-child(2) > div > div.col.pl-2::text"
        ).get().strip()

        yield {
            "title": job_title,
            "technologies": job_technologies,
        }
