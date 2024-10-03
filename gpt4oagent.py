import os
import subprocess
import requests
import pickle
import json
import asyncio
from colorama import Fore, Style
from googlesearch import search
from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
system = [
    {
        "role": "system",
        "content": "You are a computer assistant on a Debian 12 linux machine with the capability to run bash commands. "
                   "Make sure to give descriptions of the steps that you are taking when executing commands and double check your work. "
                   "You should use all the tools and problem solving available to you to accomplish a task that was given to you. Be proactive!"
    }
]


def chat_completion_request(messages, functions=None, function_call=None, model="gpt-4o-mini", max_tokens=4096):
    """Make a request to the OpenAI Chat API to generate responses."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get('OPENAI_API_KEY')
    }

    json_data = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens
    }

    if functions is not None:
        json_data.update({"functions": functions})

    if function_call is not None:
        json_data.update({"function_call": function_call})

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data
        )
        return response
    except Exception as e:
        print(Fore.RED + "Unable to generate ChatCompletion response")
        print(Fore.RED + f"Exception: {e}")
        return e


with open("functions.json", 'r') as file:
    functions = json.load(file)


def execute_function(function_name, function_args):
    print(Fore.YELLOW + Style.BRIGHT + f"Executing function: {function_name} with arguments: {function_args}" + Style.RESET_ALL)
    function_to_call = functions_dict[function_name]
    return function_to_call(**function_args)


def google_search(query):
    print(Fore.YELLOW + Style.BRIGHT + f"Searching Google for: {query}" + Style.RESET_ALL)
    urls = []

    for j in search(query, tld="com", num=15, stop=15, pause=2):
        urls.append(j)

    return urls


def run_bash_command(command):
    print(Fore.YELLOW + Style.BRIGHT + f"Running bash command: {command}" + Style.RESET_ALL)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


def fetch_links(url):
    print(Fore.YELLOW + Style.BRIGHT + f"Retrieving absolute links from {url}" + Style.RESET_ALL)
    response = session.get(url)
    return response.html.absolute_links


def fetch_website_text(url):
    print(Fore.YELLOW + Style.BRIGHT + f"Reading from {url}" + Style.RESET_ALL)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        cleaned_text = ' '.join(text.split())

        return cleaned_text
    else:
        return f"Error: Unable to fetch the website. Status code: {response.status_code}"


functions_dict = {
    "run_bash_command": run_bash_command,
    "google_search": google_search,
    "fetch_links": fetch_links,
    "fetch_website_text": fetch_website_text
}


class LLMAgent:
    def process_command(self, command):
        """Process a command and interact with the GPT-4o model."""
        try:
            if not os.path.exists("context/context.pickle"):
                with open("context/context.pickle", "wb") as write_file:
                    pickle.dump(system, write_file)

            with open("context/context.pickle", "rb") as rf:
                chathistory = pickle.load(rf)

            chathistory.append({
                "role": "user",
                "content": command
            })

            chat_response = chat_completion_request(
                chathistory,
                functions=functions
            )

            # print(chat_response.json())

            assistant_message = chat_response.json()["choices"][0]["message"]

            while "function_call" in assistant_message:
                chathistory.append(assistant_message)
                function_name = assistant_message["function_call"]["name"]
                function_args = json.loads(assistant_message["function_call"]["arguments"])
                result = execute_function(function_name, function_args)

                chathistory.append({
                    "role": "function",
                    "name": function_name,
                    "content": str(result)
                })

                chat_response = chat_completion_request(
                    chathistory,
                    functions=functions
                )

                # print(chat_response.json())

                assistant_message = chat_response.json()["choices"][0]["message"]
                chathistory.append(assistant_message)
                assistant_message_text = assistant_message["content"]
                print(Fore.BLUE + f"\n GPT-4o: {assistant_message_text} \n")

            assistant_message_text = assistant_message["content"]

            if not chathistory[-1]["content"] == assistant_message_text:
                chathistory.append(assistant_message)
                print(Fore.BLUE + f"\n GPT-4o: {assistant_message_text} \n")

            with open("context/context.pickle", "wb") as write_file:
                pickle.dump(chathistory, write_file)

        except Exception as e:
            print(Fore.RED + f"{e}")


def interactive_shell():
    """Start an interactive shell to interact with the GPT-4o model."""
    agent = LLMAgent()
    print("Starting interactive shell with GPT-4o. Type 'exit' to leave.")
    while True:
        print(Fore.GREEN + "User: ", end='')
        command = input()
        if command.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        agent.process_command(command)

if __name__ == '__main__':
    interactive_shell()
