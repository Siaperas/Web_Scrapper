import sys
import os
sys.path.append(os.getcwd())
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

#Starting URL
baseURL = 'https://www.theguardian.com/international'

'''
Converts a selenium driver object to a BeautifulSoup object
by first encoding the page source code into ascii and by ignoring any
unknown characters'''
def convert_webdriver_to_soup(driver):
    html = (driver.page_source).encode('ascii', 'ignore')
    soup = BeautifulSoup(html, 'lxml')
    return soup

'''
The function responsible to set the driver and any other
necessary options
'''
def set_driver():
    options = webdriver.ChromeOptions()
    p=r"chromedriver.exe"
    driver = webdriver.Chrome(executable_path=p, chrome_options=options)
    return driver

#Function which visits a specifc URL
def go_to_URL(baseURL, driver):
    driver.get(baseURL)
    driver.maximize_window()
    return driver

#Scrape the title and the link of the news site you scrapping
def scrape(soup, df_dump):
    #Change class names depending on page
    link_class='fc-item__link'
    title_class='js-headline-text'
    data = soup.findAll('a',attrs={'class':link_class})
    linksdata=[]
    for d in data:
        linksdata.append(d['href'])
    data2 = soup.findAll('span', attrs={'class': title_class})
    titledata=[]
    for d in data2:
        titledata.append(d.text)

    df1 = pd.DataFrame({'Titles': titledata,'Links':linksdata})
    print df1



def run():
    start_time = time.time()
    df_dump = pd.DataFrame()
    driver = set_driver()
    go_to_URL(baseURL, driver)
    time.sleep(2)
    soup = convert_webdriver_to_soup(driver)
    df_dump = scrape(soup, df_dump)
    driver.quit()
    print("--- %s seconds ---" % (time.time() - start_time))

run()