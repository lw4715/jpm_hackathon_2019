import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

url = 'https://twitter.com/unloggeddiving?lang=en'

pause = 10

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('/Users/linna/Development/chromedriver', chrome_options=chrome_options)
driver.get(url)
#This code will scroll down to the end
for i in range(5):
	try:
		# Action scroll down
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		print("Scrolling...")
		time.sleep(5)
	except: 
		pass

print("DONE SCROLLING!")



tweets_unique = {}

response = driver.page_source

soup = BeautifulSoup(response, "html.parser")
tweets_raw = soup.findAll('div', {"class": "tweet"})

print("Size:", len(tweets_raw))
for tweet_raw in tweets_raw:
	data_tweet_id = tweet_raw.attrs['data-tweet-id']
	print("ID:", data_tweet_id)
	time_div = tweet_raw.find('span', {'class': '_timestamp'}, recusive=False).attrs['data-time-ms']
	print(time_div, datetime.datetime.utcfromtimestamp(int(time_div)/1000))
	username = tweet_raw.find('span', {'class': 'username'}, recusive=False).find("b").text
	print(username)
	tweet_text = tweet_raw.find('p', {'class': 'tweet-text'}).text
	print(tweet_text)
	tweets_unique[data_tweet_id] = {"username": username, "ts": time, "tweet_text": tweet_text}
	print('-----')

# print("///////")
print(len(tweets_unique), len(tweets_raw))