from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import random

HEADERS = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

class Crawler:
    base_url = ""
    search_addr = "/search"
    def __init__(self):
        pass

    def search(self, params):
        response = requests.get(self.base_url+self.search_addr, params=params, headers={'User-Agent':random.choice(HEADERS)})
        return BeautifulSoup(response.text, 'html.parser')

class NTCrawler(Crawler):
    base_url = "https://www.nytimes.com"
    search_addr = "/search"

    def search_today(self, query):
        date = datetime.now().strftime("%Y%m%d")
        return self.search({"dropmab":"true","endDate":date,"query":query,
                            "sort":"best", "startDate":date})

    def search(self, params):
        soup = super().search(params)

        hyper_params = [{"data-testid":"search-results"}, ]
        child_lis = soup.find(**(hyper_params[0])).find_all('li', recursive=False)
        news = []
        for c_div in child_lis:
            title = c_div.find('h4')
            if title is None:
                continue
            url = c_div.find('a', href=True)
            defaults = {}
            defaults["title"] = title.text
            category = c_div.find('p')
            if category:
                defaults["category"] = category.text
            img = c_div.find('img')
            if img:
                defaults["image_url"] = img.get('src')
            news.append({"url":self.base_url+url['href'], 
                         "defaults":defaults})
        
        return news

class CNNCrawler(Crawler):
    base_url = "https://www.cnn.com"
    search_addr = "/search"

    def search_today(self, query):
        return self.search({"q":query,"size":10,"sort":"newest"})

    def search(self, params):
        soup = super().search(params)
        print(soup.prettify())
        fw = open("test.html","w")
        fw.write(soup.prettify())
        fw.close() 

        child_divs = soup.find_all('h3', recursive=True)
        print(child_divs)
        news = []
        for c_div in child_divs:
            title = c_div.find(class_="cnn-search__result-headline")   
            #print(title)         
            if title is None:
                continue
            url = title.find('a', href=True)
            title = url.text

            defaults = {}
            defaults["title"] = title.text
            defaults["category"] = None
            img = c_div.find('img')
            if img:
                defaults["image_url"] = img.get('src')
            news.append({"url":self.base_url+url['href'], 
                         "defaults":defaults})
        
        return news


