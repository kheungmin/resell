from selenium import webdriver
import requests
from scrapy.http import TextResponse
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymongo


# def get_chrome_driver():
#     # 1. 크롬 옵션 세팅
#     chrome_options = webdriver.ChromeOptions()
    
#     # 2. driver 생성하기
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
#         options=chrome_options
#     )
    
#     return driver

def get_chrome_driver():
    # 1. 크롬 옵션 세팅
    options = webdriver.ChromeOptions()
    
    # 2. driver 생성하기
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
        options=options
    )
    
    
    return driver





driver = get_chrome_driver()

try:
    url='https://www.instagram.com/'
    driver.get(url)
    driver.implicitly_wait(10)


    # login_id = 'heungminn@naver.com'
    # login_pw = 'multi!1234'
    # driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(login_id)
    # driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(login_pw)

    # driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]').click()



    # 접속
    # driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').click()                                
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('heungminn@naver.com')
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('multi!1234')
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/button/div').click()
    time.sleep(3)


    # 세부 접속 시 확인사항
    driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()

    driver.find_element(By.CSS_SELECTOR, '._a9_1').click()
    time.sleep(3)

    # 특정 셀럽 계정 접속
    url1='https://www.instagram.com/apfhda7/'
    driver.get(url1)
    driver.implicitly_wait(10)

    # mongoDB 접속 정보
    client = pymongo.MongoClient('mongodb://team04:1111@ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com:27017/')
    db = client.resell



    # 데이터 크롤링

    t1 =driver.find_elements(By.CSS_SELECTOR,'._aabd._aa8k._aanf > a')
    url_lst = [t.get_attribute('href') for t in t1]

    # 내부 외부 이미지 url 정제
    pattern = '/[\d_n]+\.jpg'

    db_img_url = list(db.insta.find({}, {'_id': 0, 'img_url': 1}))
    img_url_lst = [re.findall(pattern, dic['img_url'])[0] for dic in db_img_url]

    # 원하는 이미지 url 형태
    # ex) /294416712_395538335930284_918132169382424976_n.jpg

    # flag 변수 - 다중 반복문 안에서 내부 반복문 break 시 활용.
    stop = False
    for url in url_lst:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._aap6._aap7._aap8')))
        
        user = driver.find_element(By.CSS_SELECTOR, '._aap6._aap7._aap8').text
        time_raw = driver.find_element(By.CSS_SELECTOR, '._aaqe')
        write_time = pd.to_datetime(time_raw.get_attribute('datetime'))
        
        bucket = set()
        while True:
            for el in driver.find_elements(By.CSS_SELECTOR,'._aatk._aatn ._aagt'):
                url3 = el.get_attribute('src')

                img_name = re.findall(pattern, url3)[0]
                
                if img_name in img_url_lst:
                    stop = True
                    break # for el in~ 반복문 stop
                
                if url3:
                    bucket.add(url3)

            if stop:
                break # while문 stop
            
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._9zm2')))
                driver.find_element(By.CSS_SELECTOR,'._9zm2').click()
                time.sleep(1)
            except:
                break # while문 stop
        
        if stop:
            break # for url in url_lst for문 stop
        
        for img_url in bucket:
            data = {'user': user, 'write_time': write_time, 'img_url': img_url}
            db.ttt.insert_one(data)
            # print(data)
except:
    pass
finally:
    driver.quit()