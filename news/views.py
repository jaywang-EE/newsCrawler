from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from news.models import News
# Create your views here.
import json


class MainView(View) :
    def get(self, request):

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
        news = News.objects.all().values()
        news_list = list(news)
        """
        return JsonResponse(users_list, safe=False)
        user_count = User.objects.filter(active=True).count()
        """
        ctx = {'data': news_list}
        return Response(ctx)