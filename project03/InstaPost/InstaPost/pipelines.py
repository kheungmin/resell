# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class InstapostPipeline:
    def process_item(self, item, spider):
        user = 'team04'
        pw = '1111'
        host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
        client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')
        db = client.resell
        
        data = {'model_no': item['model_no'], 'img_url': item['img_url']}
        db.insta_post.insert_one(data)
        
        return item
