from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from news.models import News
from news.crawler import craw
# Create your views here.
import json


class MainView(View) :
    def get(self, request):
        craw()
        news_list = News.objects.all();

        ctx = { 'news_list': news_list };
        return render(request, 'news/news_list.html', ctx)


from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class GetJsonView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        category = request.GET.get('cat')
        fromDate = request.GET.get('fromDate')
        toDate = request.GET.get('toDate')
        count = request.GET.get('count')

        news = News.objects.all()
        if category:
            print(category)
            news = news.filter(category=category)
        #news = News.objects.filter(date__range=["2011-01-01", "2011-01-31"])[:count]
        if count: 
            news = news[:int(count)]
        news = news.values()
        news_list = list(news)
        
        """
        return JsonResponse(users_list, safe=False)
        user_count = User.objects.filter(active=True).count()
        """
        ctx = {'data': news_list, "params": {"category":category, "fromDate":fromDate, "toDate":toDate, "count":count}, "count":len(news_list)}
        return Response(ctx)