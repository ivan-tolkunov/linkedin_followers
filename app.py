from flask import Flask, request
from pydantic import BaseModel
from urllib.parse import quote_plus
import os
from functools import cache
from pathlib import Path
from PIL import Image
import imagehash
from urllib.request import urlretrieve
from linkedin_scraper import actions
from selenium.webdriver.common.by import By
import pickle
import hashlib


email = "email"
password = "password"
cookies_file_path = Path("cookies") / "cookies.pkl"

app = Flask(__name__)

class Request(BaseModel):
    linkedin_url: str


class Response(BaseModel):
    followers: int
    profile_photo_url: str
    profile_photo_hash: str

def create_driver():
    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def get_info(driver, linkedin):
    try:
        login(driver)

        driver.get(linkedin)

        driver.implicitly_wait(5)

        followers_el = driver.find_element(By.CSS_SELECTOR, '.text-body-small.t-black--light.inline-block>.t-bold')
        img_el = driver.find_element(By.CSS_SELECTOR, '.pv-top-card-profile-picture__image--show')

        followers = followers_el.text
        img_url = img_el.get_attribute('src')

        return followers, img_url
    
    except Exception as e:
        return str(e), None

def save_cookie(driver):
    with open(cookies_file_path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def login(driver):
    cookies_file_path.parent.mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(cookies_file_path):
       actions.login(driver, email, password)
       save_cookie(driver)
       return
    
    with open(cookies_file_path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            if cookie['name'] == 'li_at':
                actions.login(driver, email, password, cookie['value'])
                return
    
    actions.login(driver, email, password)
    save_cookie(driver)
            
def download_image(url):
    file_name = Path("images") / (hashlib.sha256(url.encode()).hexdigest() + ".jpg")
    file_name.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, file_name)
    return file_name

def get_image_hash(img_url):
    img_path = download_image(img_url)
    return imagehash.phash(Image.open(img_path))

@app.route('/get_follower_count', methods=['GET'])
def get_follower_count_route():
  linkedin_url = request.args.get('linkedin_url')
  if linkedin_url:
    try:
        driver = create_driver()
        followers, img_url = get_info(driver, linkedin_url)
        img_hash = get_image_hash(img_url)
        print(followers, img_url, str(img_hash))
        return {"followers": followers, "img_url": img_url, "img_hash": str(img_hash)}
    finally:
        driver.quit() 

def download_image(url):
    file_name = Path("images") / (hashlib.sha256(url.encode()).hexdigest() + ".jpg")
    print(f"Downloading {url} to {file_name}")
    file_name.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, file_name)
    return file_name

if __name__ == '__main__': 
   app.run(debug=True)