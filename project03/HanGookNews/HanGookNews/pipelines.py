# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter


class HangooknewsPipeline:
    def process_item(self, item, spider):
        user = 'team04'
        pw = '1111'
        host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
        client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')
        
        for i in range(len(item['news_title'])):
            dic = {'news_title' : item['news_title'][i],
                   'news_time' : item['news_time'][i],
                   'news_content' : item['news_content'][i]}
            
            client.resell.project_test.insert_one(dic)
        
        return item