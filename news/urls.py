from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name='news'
urlpatterns = [
    path('viz', views.MainView.as_view(), name='all'),
    path('', views.GetJsonView.as_view(), name='json'),
]

