import requests
from bs4 import BeautifulSoup
import re

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# Function to search Google and get related links (scraping Google results)
def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # Scraping Google results
        for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
            title = g.get_text()
            link = g.find_parent('a')['href']
            # Clean the Google search URL (strip /url?q= and &sa=...)
            clean_link = re.search(r'/url\?q=(.*?)&', link)
            if clean_link:
                link = clean_link.group(1)
                results.append({'title': title, 'link': link})

        return results
    except Exception as e:
        print(f"Error fetching Google search results: {e}")
        return []

# Function to search DuckDuckGo and get related links
def search_duckduckgo(query):
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('a', {'class': 'result__a'}):
            title = result.get_text()
            link = result['href']
            results.append({'title': title, 'link': link})

        return results
    except Exception as e:
        print(f"Error fetching search results: {e}")
        return []

# Function to fetch a brief description from Wikipedia (or other APIs)
def get_wikipedia_summary(query):
    try:
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}")
        if response.status_code == 200:
            data = response.json()
            if "extract" in data:
                return data["extract"]
        return "No description available."
    except Exception as e:
        print(f"Error fetching description: {e}")
        return "No description available."
