from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

URL = "https://www.nps.gov"

class Crawler:
    base_url = ""
    search_addr = "/search"
    def __init__(self):
        pass

    def search(self, params):
        response = requests.get(self.base_url+self.search_addr, params=params)
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


