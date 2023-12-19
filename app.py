from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
import re
import os

app = Flask(__name__)

def get_follower_count(linkedin):
    driver = create_driver()
    try:
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
    finally:
        driver.quit()

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
    follower_count = get_follower_count(linkedin_url)
    return {"follower_count": follower_count}
  else:
    return "No LinkedIn URL provided", 400

if __name__ == '__main__': 
   app.run(debug=True)