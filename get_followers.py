from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re
from urllib.parse import quote_plus

def read_csv_file(file_name):
  file = open(file_name, "r")
  data = file.read()
  lines = data.split("\n")
  result = []
  for line in lines:
    result.append(line.split(","))
  return result

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

  # If a match is found, print it. Otherwise, print "No match found"
  if match:
    print(match.group())
  else:
    print("No match found")

  # Close the browser
  driver.quit()

urls = read_csv_file("./test.csv")

for url in urls:
  print(url[0])
  follower_count = get_follower_count(url[0])
  print(follower_count)
  time.sleep(random.uniform(10, 30)) 