"""
URL configuration for your Django app.

This module defines the URL patterns for the application.
"""


from django.contrib import admin
from django.urls import path
from .views import greet
from .views import search_tavily

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', greet, name='greet'),
    path('search/', search_tavily, name='search_tavily'),]
