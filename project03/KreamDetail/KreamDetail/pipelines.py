# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class KreamdetailPipeline:
    def process_item(self, item, spider):
        user = 'team04'
        pw = '1111'
        host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
        client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')
        db = client.resell
        
        data = {
            'brand': item['brand'],
            '_id': item['prod_name'],
            'prod_kr_name': item['prod_kr_name'],
            'rescent_price': item['rescent_price'],
            'model_no': item['model_no'],
            'release_date': item['release_date'],
            'colors': item['colors'],
            'release_price': item['release_price'],
            'instant_buy_price': item['instant_buy_price'],
            'instant_sell_price': item['instant_sell_price'],
            'img_url': item['img_url']
        }
        
        db.kream_detail.insert_one(data)
        
        return item
