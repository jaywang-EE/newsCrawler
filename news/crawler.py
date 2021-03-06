from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import random
from news.models import News

HEADERS = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]


CACHE_FILENAME = "search_hist.json"
def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def craw():
    cache = open_cache()

    crawler = TreehuggerCrawler("/green-food", "food", "treehugger")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)

    crawler = TreehuggerCrawler("/corporate-responsibility", "corporations", "treehugger")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)

    crawler = TreehuggerCrawler("/climate-change", "climate", "treehugger")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)

    crawler = ViceCrawler("/environment", "msc", "vice")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)
    
    crawler = ThedodoCrawler("/close-to-home", "buddies", "The Dodo")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)
    
    crawler = PlasticbagbanreportCrawler("/legislation", "politics", "Plastic Bag Ban Report")
    results = crawler.search()
    for n in results:
        News.objects.update_or_create(**n)
    
    save_cache(cache)


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

class ThedodoCrawler(Crawler):
    base_url = "https://www.thedodo.com"

    def search(self):
        soup = super().search({})
        news = []

        last_section = soup.find("section", class_="double-column-listing-layout u-color--white-background")
        last_section = last_section.find("div", class_="stack__wrap")

        gutters = last_section.find_all("div", class_="frow gutters", recursive=False)

        for g in gutters:
            divs = g.find_all('section', recursive=True)
            for a in divs:
                defaults = self.defaults.copy()

                a = a.find("div", class_="frow")

                img, title = a.find_all("div", recursive=False)
                
                defaults["title"] = title.find("h2").text.strip('\n').strip(' ')

                img = img.find("a")
                defaults["image_url"] = img.find("img").get("src")

                detail_soup = super().search({}, img.get("href"))

                info_div = detail_soup.find("div", class_="meta-info__item-details")

                defaults["author"] = info_div.find("a", rel="author").text.strip()

                date = info_div.find("div", class_="author-meta-info__published-info").text.strip()

                date = date.split(" ")[-1]

                defaults["date"] = datetime.strptime(date, '%m/%d/%Y').date()

                news.append({"url":img.get("href"), 
                             "defaults":defaults})

        return news


class TreehuggerCrawler(Crawler):
    base_url = "https://www.treehugger.com"

    def search(self):
        soup = super().search({})
        news = []

        articles = soup.find(class_="c-block__cards").find_all('article', recursive=False)
        
        for a in articles:
            if 1:
                defaults = self.defaults.copy()

                title = a.find(class_="c-article__headline").find('a')
                defaults["title"] = title.text.strip('\n')

                span = a.find(class_="c-article__byline").find("span")

                defaults["author"] = span.find(rel="author").text.strip()

                date = span.find(class_="c-article__published").text.strip()
                defaults["date"] = datetime.strptime(date, '%B %d, %Y').date()
                
                defaults["image_url"] = a.find(class_="c-article__image").find("img").get('src')
                
                news.append({"url":self.base_url+title['href'], 
                             "defaults":defaults})
            try:
                pass
            except:
                print("ERROR: "+self.base_url)

        return news

class ViceCrawler(Crawler):
    base_url = "https://www.vice.com/en_us/topic"

    def search(self):
        soup = super().search({})
        news = []

        sections = soup.find(class_="topics-all").find_all('section', recursive=True)
        
        for a in sections:
            try:
                defaults = self.defaults.copy()
                defaults["title"] = a.find("h3").text.strip('\n')

                defaults["author"] = a.find(class_="byline__byline").text.strip()

                date = a.find(class_="topics-card__timestamp").text.strip()
                defaults["date"] = datetime.strptime(date, '%m.%d.%y').date()
                    
                img = a.find("a", recursive=False)
                defaults["image_url"] = img.find("source").get("srcset")
                #print(img.find("source").get("srcset"))

                news.append({"url":img.get("href"), 
                             "defaults":defaults})
            except:
                print("ERROR: "+self.base_url)

        return news
