import scrapy
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from InstaPost.items import InstapostItem


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.headless = True

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver


class Spider(scrapy.Spider):
    name = 'InstaPost'
    allow_domain = ['https://kream.co.kr']
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    
    start_urls = ['https://kream.co.kr']
    
    
    def __init__(self):
        self.product_lst = [
            {'model_no': 'DD9315-002', 'link': 'https://kream.co.kr/social/products/48705'},
            {'model_no': '554724-078', 'link': 'https://kream.co.kr/social/products/47257'},
            {'model_no': 'DD9315-600', 'link': 'https://kream.co.kr/social/products/48708'},
            {'model_no': '555088-063', 'link': 'https://kream.co.kr/social/products/45326'},
            {'model_no': 'DB4612-300', 'link': 'https://kream.co.kr/social/products/25833'},
            {'model_no': 'B37571', 'link': 'https://kream.co.kr/social/products/12491'},
            {'model_no': 'FV2831', 'link': 'https://kream.co.kr/social/products/36113'},
            {'model_no': '150206C', 'link': 'https://kream.co.kr/social/products/23509'},
            {'model_no': 'DJ7840-002', 'link': 'https://kream.co.kr/social/products/60294'},
            {'model_no': 'DR5475-100', 'link': 'https://kream.co.kr/social/products/59516'},
            {'model_no': 'DV3501-400', 'link': 'https://kream.co.kr/social/products/57895'},
            {'model_no': 'CJ9179-200', 'link': 'https://kream.co.kr/social/products/21935'},
            {'model_no': 'DO9392-200', 'link': 'https://kream.co.kr/social/products/44512'},
            {'model_no': 'DJ4877-300', 'link': 'https://kream.co.kr/social/products/43767'},
            {'model_no': 'DD1877-002', 'link': 'https://kream.co.kr/social/products/38231'}
        ]
        
    
    def parse(self, response):
        for product in self.product_lst:
            driver = get_chrome_driver()
            driver.implicitly_wait(10)
            driver.maximize_window()
            
            driver.get(product['link'])
            
            # 무한스크롤
            scroll_cnt = 0
            same_cnt = 0
            while True:
                cur_height = driver.execute_script('return document.body.scrollHeight;')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(3)
                next_height = driver.execute_script('return document.body.scrollHeight;')

                if cur_height == next_height:
                    same_cnt += 1
                    if same_cnt >= 3:
                        break
                else:
                    same_cnt = 0
                    
                scroll_cnt += 1
                
                if scroll_cnt > 40:
                    break
            
            img_tags = driver.find_elements(By.CSS_SELECTOR, '.social_img')
            img_urls = [img_tag.get_attribute('src') for img_tag in img_tags]
            
            for img_url in img_urls:
                item = InstapostItem()
                
                item['model_no'] = product['model_no']
                item['img_url'] = img_url
                
                yield item
                
                del item
            
            driver.quit()
            
            time.sleep(10)