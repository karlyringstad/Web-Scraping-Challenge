# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from flask import Flask, render_template
import time
import re
import pymongo
from selenium import webdriver


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    
    
    # NASA Mars News
    
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Collect the latest News Title
    news_title = soup.find('div', class_="content_title").text

    # Collect the latest Paragraph Text
    news_p = soup.find("div", class_="rollover_description_inner").text
    
    

    # JPL Mars Space Images - Featured Image

    browser = init_browser()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Create HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all elements that contain image information
    images = soup.find_all('a', class_ = "fancybox")

    # Pull the featured image link
    url_list = []
    for image in images:
        href = image['data-fancybox-href']
        url_list.append(href)

    featured_image_url = 'https://www.jpl.nasa.gov' + href

    

    # Mars Weather

    # Visit the Mars Weather twitter account
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(twitter_url)

    # Create HTML object
    soup = BeautifulSoup(response.text,'html.parser')


    tweets = soup.find_all("div", class_="js-tweet-text-container")

    # Extract title text
    weather_tweets = []
    for weather in tweets:
        tweet = weather.text
        weather_tweets.append(tweet)


    mars_weather = re.sub(r'pic.twitter.com\S+', '', weather_tweets[0].replace('\n',' ').lstrip())
    
    

    # Mars Facts

    # Mars Facts URL
    mars_facts_url = "https://space-facts.com/mars"

    # Scrape table
    table = pd.read_html(mars_facts_url)

    # Create df for table
    facts_df = table[0]
    facts_df.columns = ['Facts', 'Value']

    # Use Pandas to convert the data to a HTML table string
    facts_html = facts_df.to_html(index=False)

    
    
    # Mars Hemispheres

    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Retrieve page with the requests module
    response = requests.get(mars_hem_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all('a', class_="itemLink product-item")

    # Create list to store images
    hemisphere_image_urls = []

    # Iterate through images and scrape the website
    for image in images:
        hem_image_dict = {}
        title = image.find('h3').text
        hem_image_dict['Title'] = title.strip('Enhanced')
        temp_img_url = image['href']
        image_url = 'https://astrogeology.usgs.gov' + temp_img_url
        request = requests.get(image_url)
        soup = BeautifulSoup(request.text, 'lxml')
        tag = soup.find('div', class_ = 'downloads')
        img_url = tag.find('a')['href']
        hem_image_dict['img_url'] = img_url


        hemisphere_image_urls.append(hem_image_dict)


    # Make a dictionary
    mars_info = {
        "news_title": news_title,
        'news_p' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_current_weather' : mars_weather,
        'mars_facts' : facts_html,
        'hemisphere_image_urls' : hemisphere_image_urls
    }
        

    
    return mars_info

