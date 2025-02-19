"""
This module defines views for the 'calc' app, including the functionality to search
the Tavily API and handle user queries.

It contains the following views:
- greet: Displays a greeting message based on user input.
- search_tavily: Handles search functionality by sending queries to the Tavily API.
"""

import json
import requests
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from tavily import TavilyClient
from .models import SearchResult


def greet(request):
    """
    Handles the search functionality by making a POST request to the Tavily API.
    """
    message = ""
    if request.method == "POST":
        name = request.POST.get("name")
        message = f"Hello, {name}!"
    return render(request, "usergreet.html", {"message": message})



# new code


@csrf_exempt
def search_tavily(request):
    """Fetches search results from Tavily API and displays them in the frontend."""

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
    query = request.POST.get('search_query', '').strip()  # Get search query

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
        data = json.loads(request.body)
        selected_results = data.get("results", [])

        # Save selected results to the database (Example Model)
        for item in selected_results:
            SearchResult.objects.create(title=item['title'], url=item['url'], content=item['content'])

        return JsonResponse({"message": "Results saved successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)
