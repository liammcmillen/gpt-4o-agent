from .DebugLogger import DebugLogger
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from googlesearch import search
import requests

class WebSearcher:
    def __init__(self, user_agent: str):
        self.headers = {'User-Agent': user_agent}

    @staticmethod
    def google_search(query):
        DebugLogger.log(f"Performing Google search for: {query}", level='SYSTEM')
        urls = list(search(query, tld='com', num=15, stop=15, pause=2))
        DebugLogger.log(f"Search results: {urls}", level='INFO')
        return urls

    @staticmethod
    def fetch_links(url):
        DebugLogger.log(f"Fetching links from URL: {url}", level='SYSTEM')
        session = HTMLSession()
        try:
            response = session.get(url)
            DebugLogger.log(f"HTTP status from fetching links: {response.status_code}", level='INFO')
            DebugLogger.log(f"Retrieved links: {response.html.absolute_links}", level='INFO')
            return list(response.html.absolute_links)
        except Exception as e:
            error_msg = f"Error fetching links from URL: {e}"
            DebugLogger.log(error_msg, level='ERROR')
            return []

    @staticmethod
    def fetch_website_text(url):
        DebugLogger.log(f"Fetching text from URL: {url}", level='SYSTEM')
        try:
            response = requests.get(url)
            DebugLogger.log(f"HTTP status code: {response.status_code}", level='INFO')
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                full_text = soup.get_text(separator=' ', strip=True)
                DebugLogger.log(f"Fetched text preview: {full_text[:200]}", level='INFO')
                return full_text
            else:
                error_msg = f'Error: Unable to fetch the website. Status code: {response.status_code}'
                DebugLogger.log(error_msg, level='ERROR')
                return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Request exception: {e}"
            DebugLogger.log(error_msg, level='ERROR')
            return error_msg