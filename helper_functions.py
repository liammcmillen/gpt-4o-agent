import os
import subprocess
import requests
from colorama import Fore, Style
from googlesearch import search
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

def chat_completion_request(messages, functions=None, function_call=None, model='gpt-4o-mini', max_tokens=4096):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ.get('OPENAI_API_KEY')
    }

    json_data = {
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens
    }

    if functions is not None:
        json_data.update({'functions': functions})

    if function_call is not None:
        json_data.update({'function_call': function_call})

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=json_data
        )
        return response
    except Exception as e:
        print(Fore.RED + 'Unable to generate ChatCompletion response')
        print(Fore.RED + f'Exception: {e}')
        return e

def execute_function(function_name, function_args):
    print(Fore.YELLOW + Style.BRIGHT + f'Executing function: {function_name} with arguments: {function_args}' + Style.RESET_ALL)
    function_to_call = functions_dict[function_name]
    return function_to_call(**function_args)

def google_search(query):
    print(Fore.YELLOW + Style.BRIGHT + f'Searching Google for: {query}' + Style.RESET_ALL)
    urls = []

    for j in search(query, tld='com', num=15, stop=15, pause=2):
        urls.append(j)

    return urls

def run_bash_command(command):
    print(Fore.YELLOW + Style.BRIGHT + f'Running bash command: {command}' + Style.RESET_ALL)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

def fetch_links(url):
    print(Fore.YELLOW + Style.BRIGHT + f'Retrieving absolute links from {url}' + Style.RESET_ALL)
    response = session.get(url)
    return response.html.absolute_links

def fetch_website_text(url):
    print(Fore.YELLOW + Style.BRIGHT + f'Reading from {url}' + Style.RESET_ALL)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        cleaned_text = ' '.join(text.split())

        return cleaned_text
    else:
        return f'Error: Unable to fetch the website. Status code: {response.status_code}'

functions_dict = {
    "run_bash_command": run_bash_command,
    "google_search": google_search,
    "fetch_links": fetch_links,
    "fetch_website_text": fetch_website_text
}
