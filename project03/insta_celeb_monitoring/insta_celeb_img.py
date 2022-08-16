import re
import time
import pymongo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chrome_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    return driver


driver = get_chrome_driver()

try:
    url ='https://www.instagram.com/'
    driver.get(url)
    driver.implicitly_wait(10)

    # 로그인
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('heungminn@naver.com')
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('multi!1234')
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button/div').click()
    time.sleep(3)

    # 특정 셀럽 계정 접속
    user = 'apfhda7'
    url1 = 'https://www.instagram.com/apfhda7/'
    driver.get(url1)

    # 원하는 이미지 url 형태
    # ex) /294416712_395538335930284_918132169382424976_n.jpg
    pattern = '/[\d_n]+\.jpg'

    # mongoDB 접속 정보
    client = pymongo.MongoClient('mongodb://team04:1111@ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com:27017/')
    db = client.resell
    db_img_url = list(db.insta.find({}, {'_id': 0, 'img_url': 1}))
    img_url_lst = [re.findall(pattern, dic['img_url'])[0] for dic in db_img_url]

    t1 = driver.find_elements(By.CSS_SELECTOR,'._aabd._aa8k._aanf > a')
    url_lst = [t.get_attribute('href') for t in t1]

    stop = False
    for url in url_lst:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._aatk._aatn ._aagt')))

        bucket = set()
        while True:
            for el in driver.find_elements(By.CSS_SELECTOR, '._aatk._aatn ._aagt'):
                url3 = el.get_attribute('src')

                img_name = re.findall(pattern, url3)[0]
                
                if img_name in img_url_lst:
                    stop = True
                    break
                
                if url3:
                    bucket.add(url3)

            if stop:
                break
            
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._9zm2')))
                driver.find_element(By.CSS_SELECTOR,'._9zm2').click()
                time.sleep(1)
            except:
                break
        
        if stop:
            break
        
        for img_url in bucket:
            data = {'user': user, 'img_url': img_url, 'new': 1}
            db.insta.insert_one(data)
except Exception as e:
    print(e)
finally:
    driver.quit()