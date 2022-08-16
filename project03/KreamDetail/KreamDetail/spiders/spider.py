import scrapy
from scrapy.http import TextResponse
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import pymongo
import time

from KreamDetail.items import KreamdetailItem


class Spider(scrapy.Spider):
    name = 'KreamDetail'
    allow_domain = ['https://kream.co.kr']
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    
    
    def __init__(self):
        self.user = 'team04'
        self.pw = '1111'
        self.host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
        self.client = pymongo.MongoClient(f'mongodb://{self.user}:{self.pw}@{self.host}:27017/')
        self.db = self.client.resell
        # self.links = list(self.db.kream.find({}, {'_id': 1, 'link': 1}))
        self.links = list(self.db.kream_detail_remain.find({}, {'_id': 1, 'link': 1}))
        
    
    def start_requests(self):
        for link_dic in self.links:
            link = link_dic['link']
            yield scrapy.Request(link, self.parse)
    
    
    def parse(self, response):
        try:
            brand = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/a/text()').extract()[0]
            prod_name = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[1]/text()').extract()[0]
            prod_kr_name = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[2]/text()').extract()[0]
            rescent_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[1]/text()').extract()[0]
            model_no = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[1]/dd/text()').extract()[0]
            release_date = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[2]/dd/text()').extract()[0]
            colors = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[3]/dd/text()').extract()[0]
            release_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[4]/dd/text()').extract()[0]
            instant_buy_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[1]/div/span[1]/em/text()').extract()[0]
            instant_sell_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[2]/div/span[1]/em/text()').extract()[0]
            soup = BeautifulSoup(response.css('#__layout picture').extract()[0])
            img_url = soup.select_one('img')['src']
        except:
            # Request again
            headers = {
                'user-agent': UserAgent().chrome
            }
            request_count = 0
            
            while not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/a/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[1]/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[2]/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[1]/dd/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[2]/dd/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[3]/dd/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[4]/dd/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[1]/div/span[1]/em/text()').extract()\
            or not response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[2]/div/span[1]/em/text()').extract():
                time.sleep(3)
                response = requests.get(response.url, headers=headers)
                response = TextResponse(response.url, body=response.text, encoding='utf-8')
                request_count += 1
                
                if request_count > 3:
                    # self.db.kream_detail_remain.insert_one({'link': response.url})
                    self.db.kream_detail_remain_remain.insert_one({'link': response.url})
                    
                    return
                
            brand = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/a/text()').extract()[0]
            prod_name = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[1]/text()').extract()[0]
            prod_kr_name = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/p[2]/text()').extract()[0]
            rescent_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/span[1]/text()').extract()[0]
            model_no = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[1]/dd/text()').extract()[0]
            release_date = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[2]/dd/text()').extract()[0]
            colors = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[3]/dd/text()').extract()[0]
            release_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[4]/dd/text()').extract()[0]
            instant_buy_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[1]/div/span[1]/em/text()').extract()[0]
            instant_sell_price = response.xpath('//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div[3]/div/a[2]/div/span[1]/em/text()').extract()[0]
            soup = BeautifulSoup(response.css('#__layout picture').extract()[0])
            img_url = soup.select_one('img')['src']
        
        item = KreamdetailItem()
        item['brand'] = brand
        item['prod_name'] = prod_name.strip()
        item['prod_kr_name'] = prod_kr_name
        item['rescent_price'] = rescent_price
        item['model_no'] = model_no
        item['release_date'] = release_date
        item['colors'] = colors
        item['release_price'] = release_price
        item['instant_buy_price'] = instant_buy_price
        item['instant_sell_price'] = instant_sell_price
        item['img_url'] = img_url
        
        yield item