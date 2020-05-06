from django.test import TestCase
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import random
# Create your tests here.

HEADERS = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

class Crawler:
    base_url = ""
    
    def __init__(self, search_addr, category, source):
        self.search_addr = search_addr
        """
        self.category = category
        self.source = source
        """
        self.defaults = {"category":category, "source":source}
        #raise NotImplementedError

    def search(self, params, url=None):
        if url is None:
            url = self.base_url+self.search_addr
        response = requests.get(url, params=params, headers={'User-Agent':random.choice(HEADERS)})
        return BeautifulSoup(response.text, 'html.parser')

class PlasticbagbanreportCrawler(Crawler):
    base_url = "http://plasticbagbanreport.com/category"


    def search(self):
        soup = super().search({})
        
        news = []

        sections = soup.find(id="content-wrap").find_all('article', recursive=False)
        
        for a in sections:
            defaults = self.defaults.copy()
            
            defaults["image_url"] = a.find(itemprop="url")["content"]
            
            header = a.find("h2").find("a")
            defaults["title"] = header.text

            defaults["author"] = a.find(itemprop="author").find("span").text

            defaults["date"] = datetime.strptime(a.find("time").text, '%Y/%m/%d').date()
            
            news.append({"url":header.get("href"), 
                         "defaults":defaults})
            
        return news

crawler = PlasticbagbanreportCrawler("/legislation", "politics", "Plastic Bag Ban Report")
results = crawler.search()
print(results)