# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo


class KreamsitePipeline:
    def process_item(self, item, spider):
        user = 'team04'
        pw = '1111'
        host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
        client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')

        data = {
            'brand': item['brand'],
            '_id': item['name'],
            'kr_name': item['kr_name'],
            'price': item['price'],
            'like': item['like'],
            'post': item["post"],
            'all_trade': item["all_trade"],
            'link' : item["link"]}

        client.resell.kream.insert_one(data)

        return item
