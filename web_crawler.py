import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import json

# {"username": username, "ts": time, "retweets": retweets, "likes": likes, "tweet_text": tweet_text}
def write_to_file(data):
	f = open("data/twitter_jpm_" + str(int(time.time())) + ".tsv","w+")
	print("Writing to file", len(data))
	for tweet_id in data.keys():
		f.write(str(tweet_id) + "\t" + str(data[tweet_id]) + "\n")
	f.close()

earliest_time = -1
start_date_str = "2015-06-01"
start_date_unix = time.mktime(datetime.datetime.strptime(start_date_str, "%Y-%m-%d").timetuple())

while(earliest_time < 0 or start_date_unix < earliest_time):

	url = 'https://twitter.com/search?q=jpm%20since%3A' + start_date_str + '%20until%3A2018-06-30&src=typd&lang=en'

	MAX_SCROLLS = 100

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('/Users/linna/Development/chromedriver', chrome_options=chrome_options)
	driver.get(url)
	#This code will scroll down to the end
	for i in range(MAX_SCROLLS):	
		# Action scroll down
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		print(str(i) + " Scrolling...")
		time.sleep(2)

	print("DONE SCROLLING!")



	tweets_unique = {}

	response = driver.page_source

	soup = BeautifulSoup(response, "html.parser")
	tweets_raw = soup.findAll('div', {"class": "tweet"})

	print("Size:", len(tweets_raw))
	for tweet_raw in tweets_raw:
		tweet_text = tweet_raw.find('p', {'class': 'tweet-text'}).text
		if ("jpm" in tweet_text.lower()):
			tweet_text = tweet_text.replace('\n', ' ').replace('\t', ' ')
			data_tweet_id = tweet_raw.attrs['data-tweet-id']
			time_div = tweet_raw.find('span', {'class': '_timestamp'}).attrs['data-time-ms']
			username = tweet_raw.find('span', {'class': 'username'}).find("b").text
			retweets = tweet_raw.find('div', {'class': 'ProfileTweet-action--retweet'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
			likes = tweet_raw.find('div', {'class': 'ProfileTweet-action--favorite'}).find('span', {'class': 'ProfileTweet-actionCountForPresentation'}).text
			earliest_time = int(time_div)/1000
			tweets_unique[data_tweet_id] = str(username)+"\t"+str(earliest_time)+"\t"+str(retweets)+"\t"+str(likes)+"\t"+str(tweet_text)
			
			# print("ID:", data_tweet_id)
			# print(time_div, datetime.datetime.utcfromtimestamp(int(time_div)/1000))
			# print("u", username, "retweets:", retweets, "likes:", likes, "tweet", tweet_text)
			# print()
			# print('-----')
		# else:
		# 	print("tweet has no jpm:", tweet_text)
		# 	print('-----')

	print("after filter count:", len(tweets_unique), "scraped count:", len(tweets_raw))
	print("Latest time unix", earliest_time, datetime.datetime.utcfromtimestamp(earliest_time))
	write_to_file(tweets_unique)
