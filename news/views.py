from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from news.models import News
from news.crawler import NTCrawler, CNNCrawler, TreehuggerCrawler, ViceCrawler, ThedodoCrawler, PlasticbagbanreportCrawler
# Create your views here.
import json

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

class MainView(View) :
    def get(self, request):
        cache = open_cache()

        crawler = TreehuggerCrawler("/green-food", "food")
        results = crawler.search()
        for n in results:
            News.objects.update_or_create(**n)

        crawler = TreehuggerCrawler("/corporate-responsibility", "corporations")
        results = crawler.search()
        for n in results:
            News.objects.update_or_create(**n)

        crawler = TreehuggerCrawler("/climate-change", "climate")
        results = crawler.search()
        for n in results:
            News.objects.update_or_create(**n)

        crawler = ViceCrawler("/environment", "msc")
        results = crawler.search()
        for n in results:
            News.objects.update_or_create(**n)
        
        crawler = ThedodoCrawler("/close-to-home", "buddies")
        results = crawler.search()
        
        for n in results:
            News.objects.update_or_create(**n)

        """
        crawler = PlasticbagbanreportCrawler("/legislation", "politics")
        results = crawler.search()
        for n in results:
            News.objects.update_or_create(**n)

        if "NYTimes" not in cache:
            cache["NYTimes"] = {"time": 0}

        if cache["NYTimes"]["time"] == 0:
            crawler = NTCrawler()
            results = crawler.search_today("environment")
            
            for n in results:
                News.objects.update_or_create(**n)
            cache["NYTimes"]["time"] = 10
        else:
            cache["NYTimes"]["time"] -= 1
        """

        save_cache(cache)
        news_list = News.objects.all();

        ctx = { 'news_list': news_list };
        return render(request, 'news/news_list.html', ctx)
