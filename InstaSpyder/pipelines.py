# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class InstaspyderPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.InstaSpyder

    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        collection.insert_one(dict(item))
        return item

class InstaspyderImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item['media_url']:        
            try:
                yield Request(item['media_url'])
            except Exception as e:
                print(e)


    def item_completed(self, results, item, info):
        item['media_url'] = [itm[1] for itm in results if itm[0]]
        return item