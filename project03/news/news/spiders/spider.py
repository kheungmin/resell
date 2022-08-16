from xml.dom.minidom import Element
import scrapy
import pymongo
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from scrapy.http import TextResponse
from fake_useragent import UserAgent
from news.items import NewsItem
from selenium.webdriver.common.keys import Keys

def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.headless = True

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver

#spider 상속
class Spider(scrapy.Spider):
    name = 'news'
    allow_domain =['bigkinds.or.kr']
    start_urls = ['https://www.bigkinds.or.kr']
    # fakeuser 설정
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    def __init__(self):
        self.url = "https://www.bigkinds.or.kr/v2/news/index.do"

    def parse(self, response):
        item = NewsItem()
        
        driver = get_chrome_driver()
        driver.implicitly_wait(10)
        driver.maximize_window()
        
        driver.get(self.url)

        # 매일경제, 한국경제 클릭
        driver.find_element(By.CSS_SELECTOR,"#category_provider_list > li:nth-child(12) > span > label").click()
        driver.find_element(By.CSS_SELECTOR,"#category_provider_list > li:nth-child(18) > span > label").click()

        # 기간선택
        driver.find_element(By.CSS_SELECTOR,"#collapse-step-1-body > div.srch-detail.v2 > div > div.tab-btn-wp1 > div.tab-btn-inner.tab1 > a").click()
        
        # 달력선택
        driver.find_element(By.CSS_SELECTOR,"#srch-tab1 > div > div.item-input > div > div:nth-child(1) > img").click()

        # 연도 변경
        for i in range(0, 4):
            driver.find_element(By.CSS_SELECTOR,"#ui-datepicker-div > div > a.year-prev").click()
            time.sleep(0.2)

        # 월 변경
        for j in range(0,3):
            driver.find_element(By.CSS_SELECTOR,"#ui-datepicker-div > div > a.ui-datepicker-prev.ui-corner-all").click()
            time.sleep(0.2)

        # 일 선택
        driver.find_element(By.CSS_SELECTOR,"#ui-datepicker-div > table > tbody > tr:nth-child(1) > td:nth-child(2) > a").click()

        driver.find_element(By.CSS_SELECTOR,"#total-search-key").click()
        
        # 검색
        searching = driver.find_element(By.CSS_SELECTOR,"#total-search-key")
        searching.send_keys('리셀', Keys.RETURN)

        time.sleep(5)

        # 보기 정렬 변경
        driver.find_element(By.CSS_SELECTOR,"#select2").click()
        driver.find_element(By.CSS_SELECTOR,"#select2 > option:nth-child(4)").click()

        time.sleep(7)
        
        test_list = []
        test_list2 = []
        
        # 뉴스 기사 이름, 뉴스 작성 시간 가져오기
        # 페이지 넘기기 (enter키 활용)
        for m in range(1, 6):            
            driver.find_element(By.CSS_SELECTOR,"#paging_news_result").clear()
            page = driver.find_element(By.CSS_SELECTOR,"#paging_news_result")
            page.send_keys(m, Keys.RETURN)
            time.sleep(5)
            news_links = driver.find_elements(By.CSS_SELECTOR, "#news-results > div > div > div.cont > a > div > strong > span")

            # 뉴스 기사 이름, 뉴스 작성 시간
            for k in range(1, len(news_links)+1):                     
                # item['news_title'] = driver.find_element(By.CSS_SELECTOR,f"#news-results > div:nth-child({k}) > div > div.cont > a > div > strong > span").text
                # item['news_time'] = driver.find_element(By.CSS_SELECTOR,f"#news-results > div:nth-child({k}) > div > div.cont > div > p:nth-child(2)").text

                test_list.append(driver.find_element(By.CSS_SELECTOR,f"#news-results > div:nth-child({k}) > div > div.cont > a > div > strong > span").text)
                test_list2.append(driver.find_element(By.CSS_SELECTOR,f"#news-results > div:nth-child({k}) > div > div.cont > div > p:nth-child(2)").text)


        item['news_title'] = test_list
        item['news_time'] = test_list2
        
        return item