from urllib.request import urlretrieve
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from PIL import Image
from pathlib import Path
import imagehash
import hashlib
import re
import os
from functools import cache

app = Flask(__name__)

def get_follower_count(driver, linkedin):
    linkedin_encoded = quote_plus(linkedin)
    driver.get(f"https://www.google.com/search?q={linkedin_encoded}")

    driver.implicitly_wait(5)

    html_content = driver.page_source

    match = re.search(r'\s*\d+(.\d+)?(K|M)?\+\s*followers', html_content)

    if match:
        s = match.group().replace(' followers', '').replace('+', '')
        return parse_number(s)
    else:
        return 0

@cache
def create_driver():
    try:
        s=Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=s)
    except:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(service=Service(os.environ.get("CHROMEDriver_PATH")), options=chrome_options)

def parse_number(num):
    if num[-1] == 'K':
        return int(float(num[:-1]) * 1000)
    elif num[-1] == 'M':
        return int(float(num[:-1]) * 1000000)
    else:
        return int(num)
    

@app.route('/get_follower_count', methods=['GET'])
def get_follower_count_route():
  linkedin_url = request.args.get('linkedin_url')
  if linkedin_url:
    try:
        driver = create_driver()
        follower_count = get_follower_count(driver, linkedin_url)
        img_link = get_img(driver, linkedin_url)
    finally:
        driver.quit() 
        
    img_path = download_image(img_link)
    hash = imagehash.phash(Image.open(img_path))
    print("hash", hash)
    return {"follower_count": follower_count,
            "profile_img_link": img_link,    
            "profile_img_hash_p": str(hash)}
  else:
    return "No LinkedIn URL provided", 400

def download_image(url):
    file_name = Path("images") / (hashlib.sha256(url.encode()).hexdigest() + ".jpg")
    print(f"Downloading {url} to {file_name}")
    file_name.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, file_name)
    return file_name

 
def get_img(driver, linkedin):
    driver.get(linkedin)

    driver.implicitly_wait(5)

    html_content = driver.page_source

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all("div", {"class": "contextual-sign-in-modal__screen contextual-sign-in-modal__context-screen flex flex-col my-4 mx-3"})
        img_link = img_from_divs(divs)
        return img_link[0]
    
    return "No HTML content found"

def img_from_divs(divs):
    images = []
    for div in divs:
        img_tags = div.find_all('img')
        for img in img_tags:
            if img.has_attr('src'):
                images.append(img['src'])
    if len(images) == 0: 
       return "No images found"
   
    return images
   

if __name__ == '__main__': 
   app.run(debug=True)