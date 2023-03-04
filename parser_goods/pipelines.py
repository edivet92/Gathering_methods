# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from pymongo import MongoClient

class ParserGoodsPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parser_goods


    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)

        return item


class CastoramaImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item['img']:
            for i in item['img']:
                try:
                    yield Request('https://www.castorama.ru' + i)
                except Exception as e:
                    print(e)


    def item_completed(self, results, item, info):
        item['img'] = [itm[1] for itm in results if itm[0]]
        return item
    
