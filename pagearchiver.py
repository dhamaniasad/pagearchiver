import random
import string
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import urlparse
import urllib2
import codecs

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
    urls = dict()
    for img in soup.findAll('img', src=True):
        img_source = urllib2.urlopen(img['src']).read()
        parse_url = urlparse.urlparse(img['src'])
        urls[img['src']] = parse_url.path.split('/')[-1]
        folders_to_make = '/'.join(parse_url.path.split('/')[0:-1])
        try:
            os.makedirs(folder_path + folders_to_make)
        except OSError:
            pass
        f = open(folder_path + parse_url.path, 'wb')
        f.write(img_source)
        f.close()
    for url in urls:
        imgs = soup.findAll('img', src=url)
        for img in imgs:
            img['src'] = urls[url]
    f = codecs.open(folder_path + '/index.html', 'wb', 'utf-8')
    f.write(soup.text)
    f.close()

open_webpage('http://gizmodo.com/the-fermi-paradox-where-the-hell-are-the-other-earths-1580345495')
