from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import quote_plus

app = Flask(__name__)

def get_follower_count(linkedin):
  # Setup webdriver
  s=Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=s)
  linkedin_encoded = quote_plus(linkedin)
  driver.get(f"https://www.google.com/search?q={linkedin_encoded}")

  # Wait for the page to load
  driver.implicitly_wait(5)

  # Get follower count
  # Get the page's HTML content
  html_content = driver.page_source

  # Search for the follower count in the HTML content
  match = re.search(r'\s*\d+(.\d+)?(K|M)?\+\s*followers', html_content)

  if match:
    driver.quit()
    return match.group()
  else:
    driver.quit()
    return 0

@app.route('/get_follower_count', methods=['GET'])
def get_follower_count_route():
  linkedin_url = request.args.get('linkedin_url')
  if linkedin_url:
    follower_count = get_follower_count(linkedin_url)
    return str(follower_count)
  else:
    return "No LinkedIn URL provided", 400

if __name__ == "__main__":
  app.run(port=5000)