"""
This module defines views for the 'calc' app, including the functionality to search
the Tavily API and handle user queries.

It contains the following views:
- greet: Displays a greeting message based on user input.
- search_tavily: Handles search functionality by sending queries to the Tavily API.
"""

import json
import sqlite3
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from tavily import TavilyClient
from .models import SearchResult
from django.db import connection
from .models import Content
#from django.contrib.auth.decorators import login_required





def greet(request):
    message = ""
    if request.method == "POST":
        name = request.POST.get("name")
        message = f"Hello, {name}!"
    return render(request, "usergreet.html", {"message": message})



# new code


@csrf_exempt
def search_tavily(request):
    data = None  # Default empty response

    if request.method == "POST":
        query = request.POST.get("query")  # Get user input from form

        if query:
            api_url = "https://api.tavily.com/search"  # Make sure this URL is correct
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.TAVILY_API_KEY}",  # Fetch API key from settings
                }
            payload = {"query": query}

            try:
                response = requests.post(api_url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()  # API response

            except requests.exceptions.Timeout:
                data = {"error": "Request timed out. Please try again."}
            except requests.exceptions.RequestException as e:
                data = {"error": str(e)}
        return render(request, "apiwebsearch/websearch.html", {"data": data})


### new code for api



# Initialize TavilyClient with your API key
#from tavily import TavilyClient
#tavily_client = TavilyClient(api_key="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")

def viewsearchpage(request):
    return render(request, 'apiwebsearch/searchweb.html')

def getsearchresults(request):
    query = request.POST.get('search_query', '').strip()

# Simulated response (Replace with actual API call if needed)
    response = {
        "results": [
            {
                "title": "9 Best resources to learn Django as of 2025 - Slant",
                "url": "https://www.slant.co/topics/1032/~best-resources-to-learn-django",
                "content": "Two Scoops of Django, Django Project Tutorials, and Hackr.io are probably your best bets out of the 9 options considered. \"Beneficial for both novice and experienced Django developers\" is the primary reason people pick Two Scoops of Django over the competition.",
                "score": 0.8646883,
                "raw_content": None
            },
            {
                "title": "What are the best tutorials out there to master Django?",
                "url": "https://forum.djangoproject.com/t/what-are-the-best-tutorials-out-there-to-master-django/22660",
                "content": "I have always recommended the combination of the Official Django Tutorial and the Django Girls Tutorial as the absolute best places to get started. They really do teach you all the necessary fundamentals.",
                "score": 0.79637206,
                "raw_content": None
            },
            {
                "title": "7 Best Free Courses to learn Django Framework in Python in 2024",
                "url": "https://medium.com/javarevisited/7-free-courses-to-learn-django-framework-in-python-bd50acc8484",
                "content": "3. Walkthrough Django's Official Tutorial [Udemy Free Course]. This course is the most versatile course on our list. Basic knowledge of HTML/CSS",
                "score": 0.6994397,
                "raw_content": None
            },
            {
                "title": "Learn Django the Easy Way with These 6 Free Resources",
                "url": "https://dev.to/evergrowingdev/learn-django-the-easy-way-with-these-6-free-resources-5fla",
                "content": "YouTube has loads of awesome tutorials where you can learn Django for free in video form if you're a more visual learner. ",
                "score": 0.6778372,
                "raw_content": None
            },
            {
                "title": "My favorite courses to learn Django for Beginners in 2024",
                "url": "https://medium.com/javarevisited/my-favorite-courses-to-learn-django-for-beginners-2020-ac172e2ab920",
                "content": "Sign up\nSign in\nSign up\nSign in\nMy favorite courses to learn Django for Beginners in 2024\njavinpaul\nFollow\nJavarevisited\n--\n1\nListen\nShare\n",
                "score": 0.65914243,
                "raw_content": None
            }
        ]
    }

    return render(request, 'apiwebsearch/searchweb.html', {'results': response['results'], 'query': query})

@csrf_exempt
def save_to_database(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_results = data.get("results", [])

            for item in selected_results:
                SearchResult.objects.create(
                    title=item['title'],
                    url=item['url'],
                    content=item['content']
                )

            return JsonResponse({"message": "Results saved successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# code for table data




def database_viewer(request):
    """Fetches table names and renders the database viewer page."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]

    return render(request, "database_viewer.html", {"tables": tables})

def get_tables(request):
    """Fetches all table names from the SQLite database."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]

    return JsonResponse({"tables": tables})

def get_table_data(request):
    """Fetches data from a selected table."""
    table_name = request.GET.get("table")

    if not table_name:
        return JsonResponse({"error": "No table specified"}, status=400)

    with connection.cursor() as cursor:
        try:
            # Get column names (Fix: No parameterized query with PRAGMA)
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]

            # Get table data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
            rows = cursor.fetchall()

            return JsonResponse({"columns": columns, "rows": rows})

        except sqlite3.Error as e:
            return JsonResponse({"error": str(e)}, status=500)


# code for content studio 


def content_studio(request):
    return render(request, 'content_studio.html')


# code for content library


def content_library(request):
    # Sample data (Replace with database query)
    content_items = [
        {"type": "Audio", "title": "Podcast Episode 1", "date": "2023-10-05", "visibility": "OnlyMe"},
        {"type": "Video", "title": "Tutorial on CSS", "date": "2023-09-30", "visibility": "OnlyMe"},
        {"type": "Text", "title": "Article on AI", "date": "2023-10-10", "visibility": "OnlyMe"},
        {"type": "File", "title": "Project Report", "date": "2023-08-24", "visibility": "OnlyMe"},
    ]

    return render(request, 'content_library.html', {"content_items": content_items})


# for content-manager





#@login_required
def content_manager(request):
    contents = Content.objects.all()
    
    if request.method == "POST":
        title = request.POST.get('title')
        visibility = request.POST.get('visibility')
        content_type = request.POST.get('content_type')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        file = request.FILES.get('file')

        Content.objects.create(
            user=request.user,
            title=title,
            visibility=visibility,
            content_type=content_type,
            description=description,
            tags=tags,
            file=file
        )
        return redirect('content_manager')

    return render(request, 'content_manager.html', {'contents': contents})

