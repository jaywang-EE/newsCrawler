from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home.urls')),  # Keep
    path('admin/', admin.site.urls),  # Keep
    path('news/', include('news.urls')),  # Keep
]
