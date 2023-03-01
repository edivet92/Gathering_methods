import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://spb.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text=python"
        ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_list = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()
        for link in vacancies_list:
            yield response.follow(link, callback=self.parse_vacancy)


    def parse_vacancy(self, response:HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()


        yield ParserJobItem(
            name = vacancy_name,
            url = vacancy_url,
            salary = vacancy_salary
        )
