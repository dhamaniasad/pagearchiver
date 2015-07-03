import random
import string
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import urlparse
import urllib2

folder_name = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
cur_dir = os.curdir


def open_webpage(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    WebDriverWait(driver=driver, timeout=10)
    source = driver.page_source
    soup = BeautifulSoup(source)
    make_links_absolute(soup, url)
    folder_path = cur_dir + '/' + folder_name
    global folder_path
    os.mkdir(folder_path)
    download_images(soup)


def make_links_absolute(soup, url):
    for tag in soup.findAll('a', href=True):
        if urlparse.urlparse(tag['href']).scheme == '':
            tag['href'] = urlparse.urljoin(url, tag['href'])
    for img in soup.findAll('img', src=True):
        if urlparse.urlparse(img['src']).scheme == '':
            img['src'] = urlparse.urljoin(url, img['src'])


def download_images(soup):
    for img in soup.findAll('img', src=True):
        img_source = urllib2.urlopen(img['src']).read()
        parse_url = urlparse.urlparse(img['src'])
        folders_to_make = '/'.join(parse_url.path.split('/')[0:-1])
        print folders_to_make
        os.makedirs(folder_path + folders_to_make)
        f = open(folder_path + parse_url.path, 'r+')
        f.write(img_source)
        f.close()

open_webpage('http://www.google.com')
