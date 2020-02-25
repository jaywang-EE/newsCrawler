from django.urls import path
from . import views
from news.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
]
