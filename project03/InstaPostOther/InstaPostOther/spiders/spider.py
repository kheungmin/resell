import scrapy
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from InstaPostOther.items import InstapostotherItem


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.headless = True

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver


class Spider(scrapy.Spider):
    name = 'InstaPostOther'
    allow_domain = ['https://kream.co.kr']
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    start_urls = ['https://kream.co.kr']


    def __init__(self):
        self.url_lst = [
            'https://kream.co.kr/social/products/35897',
            'https://kream.co.kr/social/products/64588',
            'https://kream.co.kr/social/products/46734',
            'https://kream.co.kr/social/products/64448',
            'https://kream.co.kr/social/products/33815',
            'https://kream.co.kr/social/products/64586'        
        ]
    
    
    def parse(self, response):
        driver = get_chrome_driver()
        driver.implicitly_wait(10)
        driver.maximize_window()

        for url in self.url_lst:
            driver.get(url)
            
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
            
            img_tags = driver.find_elements(By.CSS_SELECTOR, '.social_img')
            img_urls = [img_tag.get_attribute('src') for img_tag in img_tags]
            
            for img_url in img_urls:
                item = InstapostotherItem()
                
                item['img_url'] = img_url
                
                yield item
                
                del item
            
        driver.quit()