"""
URL configuration for your Django app.

This module defines the URL patterns for the application.
"""


from django.contrib import admin
from django.urls import path
from .views import greet
from .views import search_tavily
from .views import viewsearchpage, getsearchresults, save_to_database

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', greet, name='greet'),
    path('search/', search_tavily, name='search_tavily'),
    path('viewsearchpage/', viewsearchpage, name='viewsearchpage'),
    path('get-results/', getsearchresults, name='getsearchresults'),
    path('save-results/', save_to_database, name='save_to_database'),
]
