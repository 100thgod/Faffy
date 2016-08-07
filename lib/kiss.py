#! /usr/bin/python

import time, mechanize

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = "http://kisscartoon.me/Cartoon/%C2%A1Mucha-Lucha/Season-01-Episode-001-Back-to-School-Weight-Gaining?id=21057"


class KissCartoon():
    def __init__(self, url, conf):
        self.url  = url
        self.conf = conf
        self.data = self.getPage(self.url)
    
    def getPage(self, url):
        br = mechanize.Browser()
        br.open(url)
        assert br.viewing_html()
        print(br)


if __name__ == "__main__":
    KissCartoon(URL, None)
