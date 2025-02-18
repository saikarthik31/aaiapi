"""
This module defines views for the 'calc' app, including the functionality to search
the Tavily API and handle user queries.

It contains the following views:
- greet: Displays a greeting message based on user input.
- search_tavily: Handles search functionality by sending queries to the Tavily API.
"""


import requests
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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
