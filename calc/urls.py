"""
URL configuration for your Django app.

This module defines the URL patterns for the application.
"""


from django.contrib import admin
from django.urls import path
from .views import greet
from . import views
from .views import search_tavily
from .views import viewsearchpage, getsearchresults, save_to_database
from .views import database_viewer, get_tables, get_table_data
from .views import content_manager


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', greet, name='greet'),
    path('search/', search_tavily, name='search_tavily'),
    path('viewsearchpage/', viewsearchpage, name='viewsearchpage'),
    path('get-results/', getsearchresults, name='getsearchresults'),
    path('save-results/', save_to_database, name='save_to_database'),
    path('content-studio/', views.content_studio, name='content_studio'),
    path('content-library/', views.content_library, name='content_library'),
    path('content/', content_manager, name='content_manager'),

]




urlpatterns += [
    path('database-viewer/', database_viewer, name='database_viewer'),
    path('get-tables/', get_tables, name='get_tables'),
    path('get-table-data/', get_table_data, name='get_table_data'),
]
