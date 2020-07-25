#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:45:48 2020

@author: carlos
"""

#web scraping
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

searchDriver = webdriver.Chrome(ChromeDriverManager().install())

searchDriver.get("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=MX&impression_search_field=has_impressions_lifetime&view_all_page_id=59139243507&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped")


usernameBox = searchDriver.find_element_by_name("email")
usernameBox.send_keys("masterchifspartan56@hotmail.com")
passwordBox = searchDriver.find_element_by_name("pass")
passwordBox.send_keys(".python1046")

try:
    loginBox = searchDriver.find_element_by_id('loginbutton')
except:
    loginBox = searchDriver.find_element_by_name('login')
loginBox.click()

searchDriver.get("https://www.facebook.com/search/pages/?q=best%20buy & filters = eyJ2ZXJpZmllZCI6IntcIm5hbWVcIjpcInBhZ2VzX3ZlcmlmaWVkXCIsXCJhcmdzXCI6XCJcIn0ifQ% 3D% 3D")

html = searchDriver.page_source

print(html)

def scrollDown(driver):
    # Get scroll height.
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom. 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # Wait to load the page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        newHeight = driver.execute_script("return document.body.scrollHeight")
        # If the browser hasn’t scrolled any more (i.e. it’s reached the end) then stop
        if newHeight == lastHeight:
            break


searchDriver.close()
