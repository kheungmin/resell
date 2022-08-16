import scrapy
import time
from KreamSite.items import KreamsiteItem
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sklearn.exceptions import DataDimensionalityWarning
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver


class Spider(scrapy.Spider):
    name = 'KreamSite'
    allow_domain = ['kream.co.kr/']
    start_urls = ['https://kream.co.kr/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    def parse(self, response):
        driver = get_chrome_driver()
        driver.set_window_size(1500, 1000)
        # 10초까지 기다린다
        driver.implicitly_wait(10)
        # 크림사이트 열기
        driver.get('https://kream.co.kr/')

        # 로그인 누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/ul/li[4]')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/ul/li[4]').click()
        # 아이디 비번치기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[1]/div/input')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[1]/div/input').send_keys('wlsgh9024@gmail.com')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/input')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/input').send_keys('multi1234!')
        # 로그인 버튼 누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[3]/a')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[3]/a').click()

        # shop누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/div[2]/div/div[1]/nav/ul/li[2]/a')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[1]/div[2]/div/div[1]/nav/ul/li[2]/a').click()
        # 카테고리 누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[1]')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[1]').click()
        # 신발 누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[1]/a/span')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[2]/div[2]/ul/li[1]/a/span').click()
        # 브랜드 누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[3]/div[1]')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[3]/div[1]').click()
        # 조던누르기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[3]/div[2]/ul/li[80]/a/span')))
        driver.find_element(
            By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]/div[1]/div[3]/div[2]/ul/li[80]/a/span').click()
        
        last_height = 0
        while True:
            # 화면 최하단으로 스크롤 다운
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            # 페이지 로드를 기다림
            time.sleep(1.5)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(1.5)

            # 새 스크롤 높이를 계산하고 마지막 스크롤 높이와 비교
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

            # 새로운 높이가 이전 높이와 변하지 않았을 경우 스크롤 종료
            if new_height == last_height:
                break

            # 스크롤 다운이 된다면 스크롤 다운이 된 후의 창 높이를 새로운 높이로 갱신
            last_height = new_height

        # 브랜드 수집
        info_brand = driver.find_elements(By.CSS_SELECTOR, '.title .brand')
        # 상품명 수집
        info_name = driver.find_elements(By.CSS_SELECTOR, '.title .name')
        # 한글 상품명 수집
        info_kr_name = driver.find_elements(By.CSS_SELECTOR, '.title .translated_name')
        # 상품 가격 수집
        info_price = driver.find_elements(By.CSS_SELECTOR, '.price .amount')
        # 찜 수집
        info_like = driver.find_elements(By.CSS_SELECTOR, '.wish_figure .text')
        # 인스타 게시물 리뷰 수집
        info_post = driver.find_elements(By.CSS_SELECTOR, '.review_figure .text')
        # 총 거래량 수 수집
        info_all_trade = driver.find_elements(By.CSS_SELECTOR, '.product')
        # 링크 수집
        info_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, '.item_inner')]
        

        info_brand_text = [x.text for x in info_brand]
        info_name_text = [x.text.strip() for x in info_name]
        info_kr_name_text = [x.text for x in info_kr_name]
        info_price_text = [x.text for x in info_price]
        info_like_text = [x.text for x in info_like]
        info_post_text = [x.text for x in info_post]
        info_all_trade_text = [x.text for x in info_all_trade]
        
        for i in range(len(info_brand_text)):
            item = KreamsiteItem()

            item["brand"] = info_brand_text[i]
            item["name"] = info_name_text[i]
            item["kr_name"] = info_kr_name_text[i]
            item["price"] = info_price_text[i]
            item["like"] = info_like_text[i]
            item["post"] = info_post_text[i]
            item["all_trade"] = info_all_trade_text[i]
            item["link"] = info_links[i]

            yield item
            
            del item

        driver.quit()
