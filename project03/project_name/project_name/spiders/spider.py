import scrapy
import json
import requests
from scrapy.http import TextResponse
from bs4 import BeautifulSoup
import os
import threading
from multiprocessing import Process
import time
from fake_useragent import UserAgent

headers = {"User-Agent" : UserAgent().chrome }
#res = requests.get(url,headers=headers)

from project_name.items import ProjectNameItem


class Spider(scrapy.Spider):
    name="project_name"
    allow_dimain=["www.mk.co.kr"]
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    
    # def get_link(self, add):
    #     link_list=[]
    #     url=f"https://www.mk.co.kr/news/economy/?page={add}"
    #     req= requests.get(url)
    #     #soup=BeautifulSoup(req.text,'html.parser')
    #     soup1=BeautifulSoup(req.content.decode('euc-kr', 'replace'), 'html.parser')
    #     response = TextResponse(req.url, body=req.text, encoding='utf-8')
    #     tt=soup1.find('div',class_='list_area')
    #     tt1 = tt.find_all('dt',class_='tit')
    
    #     for dt in tt1:
    #         link_list.append(dt.select_one('a')['href'])
    #     return link_list
        
    
    def start_requests(self):
        # url='https://www.mk.co.kr/news/economy/'
        # headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        url='https://www.mk.co.kr/news/economy/?page={}'
        res= requests.get(url,headers=headers)
        
       
    
        
        for page in range(100):
            yield scrapy.Request(url.format(page),callback=self.parse)
        
        
    def parse(self, response):
        url_list = response.xpath('//*[@class="list_area"]/dl/dt/a/@href').extract()
        
        for link in url_list:
            link = link.replace('m.mk', 'www.mk')
            #yield scrapy.Request(link, callback=self.detail_info)
            yield scrapy.Request(link,callback=self.detail_info)
        
#meta={'dont_redirect': True,'handle_httpstatus_list': [302]},

    def detail_info(self,response):
        item = ProjectNameItem()
        soup = BeautifulSoup(response.text)
        
        if response.url[8] == 'w':
            # 웹페이지
            item["article_title"]= response.xpath('//*[@id="top_header"]/div/div/h1/text()').extract_first()
            item["article_time"]= response.xpath('//*[@id="top_header"]/div/div/div[1]/ul/li[2]/text()').extract_first() 
            item["article_text"]= soup.select_one('#article_body').text 
        else :
        # elif response.url[8] == 'm':
            # 모바일페이지
            item["article_title"]= soup.select_one('div.head_tit').text #모바일
            item["article_time"] = soup.select_one('div.source_date > div:nth-child(1) > span').text
            item["article_text"]= soup.select_one('#artText').text #모바일
        # else:
        #     item["article_title"] = "None"
        #     item["article_time"] = "None" 
        #     item["article_text"] = "None"
            
        #response.url -> 웹페이지 -> 웹페이지 에서 가져오는 코드 실행
        #response.url -> 모바일페이지 -> 모바일 페이지에서 가져오는 코드
        
        # try:
        #     item["article_title"]= response.xpath('//*[@id="top_header"]/div/div/h1/text()').extract_first()   #온라인
        #     #item["article_title"]= soup.select_one('#top_header > div > div > h1').text
        # except:
        #     item["article_title"]= soup.select_one('div.head_tit').text #모바일
            
        # try:    
        #     item["article_time"]= response.xpath('//*[@id="top_header"]/div/div/div[1]/ul/li[2]/text()').extract_first() # 온라인
        #     #item["article_time"]= soup.select_one('#top_header > div > div > div.news_title_author > ul > li.lasttime1').text
        # except:
        #     #item["article_time"] = resposnse.xpath('//*[@id="wrap"]/div[2]/div/div[1]/div[1]/div[3]/div[2]/div/span/text()').extract_first() #모바일
        #     item["article_time"] = soup.select_one('div.source_date > div:nth-child(1) > span').text
        
        # #item["article_text"] = response.xpath('//*[@id="article_body"]/div/text()').extract()
        # try:
        #     item["article_text"]= soup.select_one('#article_body').text #온라인
        #    # item["article_text"]= soup.select_one('#artText').text #모바일
        # except:
        #    # item["article_text"]= soup.select_one('#article_body').text #온라인
        #     item["article_text"]= soup.select_one('#artText').text #모바일
        
        #     item["article_text"] = response.xpath('//*[@id="article_body"]/div/text()').extract()
        #response로 가져오게 되면 검은 글씨가 가져와지지 않아 text 부분은 response가 아닌 beautiful soup을 활용하여 가져온다.
        
        #soup = BeautifulSoup(response.text)
        #item["article_text"]= soup.select_one('#article_body').text
        
        # try: 
        #item["article_text"]= soup.select_one('#article_body').text
        # except:
        #     item["article_text"]= soup.select_one('#artText').text
           
        
        # except:
        #     item["article_text"] = response.xpath('//*[@id="article_body"]/div/text()').extract()
        
        
        
        #item["article_text"]= soup.select_one('#article_body > div').text
        
        yield item
        
        
        
        # try:
        #     item["article_name"]= response.xpath('//*[@id="top_header"]/div/div/h1/text()').extract_first()
        # except:
        #     item["article_name"]= response.xpath('//*[@id="top_header"]/div/div/h1/text()').extract_first().replace('…',' ').replace('·',' ')
        # try:
        #     item["article_time"]= response.xpath('//*[@id="top_header"]/div/div/div[1]/ul/li[2]/text()').extract_first()
        # except:
        #     item["article_time"]= response.xpath('//*[@id="top_header"]/div/div/div[1]/ul/li[2]/text()').extract_first().split('\xa0')[0][5:]
            
# # dict_list=[]
# for i in range(len(titles)):
#     dic={'brand': titles[i] }
#     titles[i]
#     texts[i]
#     times[i]
#     db.collection.insert_one(dic)  