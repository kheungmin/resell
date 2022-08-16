import scrapy
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from KreamTrade.items import KreamtradeItem
def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.headless = True
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver
class Spider(scrapy.Spider):
    name = 'KreamTrade'
    allow_domain = ['kream.co.kr']
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    start_urls = ['https://kream.co.kr']
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('C:/Users/gmdal/Downloads/trade_null_info_7.csv')
        self.id = 'gmdals200@naver.com'
        self.pw = '3S-mqLov'
    def parse(self, response):
        driver = get_chrome_driver()
        driver.implicitly_wait(3)
        driver.maximize_window()
        domain = 'https://kream.co.kr'
        driver.get(domain)
        # Sign in
        driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div/ul/li[4]/a').click()
        driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[1]/div/input').send_keys(f'{self.id}')
        driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/input').send_keys(f'{self.pw}')
        driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[3]/a').click()
        time.sleep(2)
        for idx in range(1, 2):
            all_trade = self.df.loc[idx, 'all_trade']
            link = self.df.loc[idx, 'link']
            try:
                '''
                    Scroll down & Trade history scraping
                '''
                driver.get(link)
                model_no = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/dl/div[1]/dd').text
                # Trade history window
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="panel1"]/a')))
                driver.find_element(By.XPATH, '//*[@id="panel1"]/a').click()
                time.sleep(1)
                # Select size
                driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div[2]/div[1]/div[2]/div/div/button/span').click()
                size_cnt = len(driver.find_elements(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/ul/li/a'))
                driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/ul/li[1]/a').click()
                time.sleep(0.5)
                for i in range(2, size_cnt + 1):
                    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div[2]/div[1]/div[2]/div/div/button/span').click()
                    time.sleep(0.5)
                    size = driver.find_element(By.XPATH, f'//*[@id="__layout"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/ul/li[4]/a')
                    if '235' not in size.text and '270' not in size.text:
                        size.click()
                        time.sleep(1)
                        continue
                    size.click()
                    time.sleep(1)
                    # Get end date
                    try:
                        driver.find_element(By.XPATH, '//*[@id="panel1"]/div/div/div[1]/div/div[3]/a/span').click()
                    except:
                        continue
                    time.sleep(1)
                    end_date = driver.find_element(By.CSS_SELECTOR, 'div.list_txt.is_active').text
                    driver.find_element(By.XPATH, '//*[@id="panel1"]/div/div/div[1]/div/div[3]/a/span').click()
                    time.sleep(1)
                    # Scroll down
                    times = 0
                    same_cnt = 0
                    pass_product = False
                    while True:
                        if all_trade > 15000:
                            if times > 100 and driver.find_elements(By.CSS_SELECTOR, 'div.list_txt.is_active')[-1].text == end_date:
                                break
                        elif all_trade > 8000:
                            if times > 20 and driver.find_elements(By.CSS_SELECTOR, 'div.list_txt.is_active')[-1].text == end_date:
                                break
                        else:
                            if driver.find_elements(By.CSS_SELECTOR, 'div.list_txt.is_active')[-1].text == end_date:
                                break
                        price_panel = driver.find_element(By.XPATH, '//*[@id="panel1"]/div/div/div[2]')
                        cur_height = driver.execute_script('return arguments[0].scrollHeight;', price_panel)
                        driver.execute_script('arguments[0].scrollTop = 0;', price_panel)
                        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', price_panel)
                        times += 1
                        if times < 20:
                            time.sleep(1)
                        elif times < 50:
                            time.sleep(2)
                        elif times < 100:
                            time.sleep(3)
                        elif times < 150:
                            time.sleep(4)
                        else:
                            time.sleep(5)
                        next_height = driver.execute_script('return arguments[0].scrollHeight;', price_panel)
                        if cur_height == next_height:
                            same_cnt += 1
                        else:
                            same_cnt = 0
                        if same_cnt >= 20:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                            pass_product = True
                            break
                    if pass_product:
                        break
                    trade_history = [trade.text for trade in driver.find_elements(By.CSS_SELECTOR, '.body_list')]
                    # Pass on to pipeline
                    for trade in trade_history:
                        item = KreamtradeItem()
                        item['model_no'] = model_no
                        item['trade'] = trade
                        yield item
                        del item
            except:
                continue
        driver.quit()