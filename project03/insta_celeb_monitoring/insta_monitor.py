import pymongo
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver


if __name__ == '__main__':
    user = 'team04'
    pw = '1111'
    host = 'ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com'
    client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/')
    db = client.resell

    db_img_url = list(db.insta.find({}, {'_id': 0, 'img_url': 1}))
    pattern = '/[\d_n]+\.jpg'
    db_img_lst = [re.findall(pattern, dic['img_url'])[0] for dic in db_img_url]

    driver = get_chrome_driver()
    driver.implicitly_wait(10)

    celeb = 'apfhda7'
    driver.get('https://www.instagram.com/apfhda7/')

    img_element_lst = driver.find_elements(By.CSS_SELECTOR, '._aagt')
    img_url_lst = [element.get_attribute('src') for element in img_element_lst]
    for img_url in img_url_lst:
        img = re.findall(pattern, img_url)[0]

        if img in db_img_lst:
            break
        else:
            data = {'user': celeb, 'img_url': img_url, 'new': 1}
            db.insta.insert_one(data)

    driver.quit()
        