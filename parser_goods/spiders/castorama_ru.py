import scrapy
from scrapy.http import HtmlResponse
from parser_goods.items import ParserGoodsItem
from scrapy.loader import ItemLoader


class CastoramaRuSpider(scrapy.Spider):
    name = "castorama_ru"
    allowed_domains = ["castorama.ru"]
    #start_urls = ["http://castorama.ru/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)        
        self.start_urls = ["https://www.castorama.ru/catalogsearch/result/?q=эхтнокактус"]

    def parse(self, response):
        links = response.xpath("//a[contains(@class, 'product-card__name')]/@href")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response:HtmlResponse):

        loader = ItemLoader(item=ParserGoodsItem(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//div[@class='price-wrapper  ']//span[@class='price']/span/span/text()")
        loader.add_xpath('img', "//ul[@class='swiper-wrapper']/li/span/@content")
        yield loader.load_item()
        


        '''
        name = response.xpath('//h1/text()').get()
        url = response.url
        price = response.xpath("//div[@class='price-wrapper  ']//span[@class='price']/span/span/text()").getall()
        img = response.xpath("//ul[@class='swiper-wrapper']/li/span/@content").getall()

        ParserGoodsItem(
            name = name,
            url = url,
            price = price,
            img = img
        )
        '''
      




