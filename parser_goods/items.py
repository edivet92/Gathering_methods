# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose


def num_price(value):
    try:
        value = list(int(value[0]))
    except:
        return value
    return value

class ParserGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(num_price), output_processor=TakeFirst())
    img = scrapy.Field()
    _id = scrapy.Field()
    
