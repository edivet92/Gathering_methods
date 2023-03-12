# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaspyderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    media_id = scrapy.Field()
    media_type = scrapy.Field()
    user_name = scrapy.Field()
    time_stamp = scrapy.Field()
    media_url = scrapy.Field()
