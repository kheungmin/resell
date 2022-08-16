import scrapy
import requests
from scrapy.http import TextResponse
from fake_useragent import UserAgent

from project_test.items import ProjectTestItem

#spider 상속
class Spider(scrapy.Spider):
    name = 'project_test'
    allow_domain =['hankyung.com']
    
    # fakeuser 설정
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
# 페이지접근 -res하지않고 parse연결 위한 정보만 yield를 이용해서 -> url을 하나씩 넘겨준다.
    def start_requests(self):
        
        for i in range(1, 101):
            url = f"https://www.hankyung.com/economy?page={i}"
            
            yield scrapy.Request(url, self.parse)
            # scrapy.Request - parse -> response
# 페이지 링크 가져오기
    def parse(self, response):
        
        # res = requests.get(response, headers=headers) -> response
        links = response.xpath('//*[@id="container"]/div[1]/div[1]/ul/li/div/h3/a/@href').extract()
        for link in links:
            
        # link가 여러개 들어가있음 - for문돌리면서 하나씩 yield를 해준다.
            yield scrapy.Request(link, self.contents)

# 내부 페이지 내용 가져오기            
    def contents(self, response):
        item = ProjectTestItem()      
        
        # 기사 제목
        item['news_title'] = response.xpath('//*[@id="container"]/div/div/article/h1/text()').extract()
        # 기사 시간
        item['news_time'] = response.xpath('//*[@id="container"]/div/div/article/div/div/div[2]/div[1]/span[1]/span/text()').extract()
        # 기사 내용 크롤링
        item['news_content'] = response.xpath('//*[@id="articletxt"]/text()').extract()
            
        
        yield item