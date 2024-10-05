import os
import json
import subprocess
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime
import streamlit as st

# Constants
SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": "You are a computer assistant on a Debian 12 linux machine with the capability to run bash commands. "
                   "Make sure to give descriptions of the steps that you are taking when executing commands and double check your work. "
                   "You should use all the tools and problem solving available to you to accomplish a task that was given to you. Be proactive! "
                   "For example, if something you have tried isn't working, try looking up the problem on google and reading through articles for help then try again."
    }
]

CHAT_HISTORY_PATH = "context"

class DebugLogger:
    LEVEL_COLOR_SCHEME = {
        'INFO': '\033[94m',  # Blue
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'API': '\033[92m',  # Green
        'SYSTEM': '\033[95m'  # Magenta
    }

    @staticmethod
    def log(message, level='INFO'):
        color = DebugLogger.LEVEL_COLOR_SCHEME.get(level, '\033[0m')
        reset_color = '\033[0m'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{level}] [{timestamp}] {message}{reset_color}")

class CommandExecutor:
    @staticmethod
    def run_bash_command(command):
        DebugLogger.log(f"Running bash command: {command}", level='SYSTEM')
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8').strip()
        stderr = result.stderr.decode('utf-8').strip()
        if result.returncode == 0:
            DebugLogger.log(f"Command succeeded with output: {stdout}", level='INFO')
        else:
            DebugLogger.log(f"Command failed with error: {stderr}", level='ERROR')
        return stdout if result.returncode == 0 else stderr

class WebSearcher:
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
                text_preview = soup.get_text(separator=' ', strip=True)[:200]
                DebugLogger.log(f"Fetched text preview: {text_preview}", level='INFO')
                return text_preview
            else:
                error_msg = f'Error: Unable to fetch the website. Status code: {response.status_code}'
                DebugLogger.log(error_msg, level='ERROR')
                return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Request exception: {e}"
            DebugLogger.log(error_msg, level='ERROR')
            return error_msg

class FunctionLoader:
    @staticmethod
    def load_functions_from_json(file_path):
        DebugLogger.log(f"Loading functions from {file_path}", level='SYSTEM')
        try:
            with open(file_path, 'r') as file:
                functions = json.load(file)
                DebugLogger.log(f"Functions loaded: {functions}", level='SYSTEM')
                return functions
        except FileNotFoundError:
            DebugLogger.log("functions.json file not found.", level='WARNING')
            return []
        except json.JSONDecodeError as e:
            DebugLogger.log(f"Error decoding JSON: {e}", level='ERROR')
            return []

class FunctionExecutor:
    FUNCTIONS_DICT = {
        "run_bash_command": CommandExecutor.run_bash_command,
        "google_search": WebSearcher.google_search,
        "fetch_links": WebSearcher.fetch_links,
        "fetch_website_text": WebSearcher.fetch_website_text
    }

    @classmethod
    def execute_function(cls, function_name, function_args):
        DebugLogger.log(f"Attempting to execute function: {function_name} with arguments: {function_args}", level='SYSTEM')
        function = cls.FUNCTIONS_DICT.get(function_name)
        if function:
            try:
                with st.spinner(f"Executing {function_name}..."):
                    result = function(**function_args)
                DebugLogger.log(f"Function {function_name} executed with result: {result}", level='INFO')
                return result
            except Exception as e:
                error_msg = f"Error executing function {function_name}: {e}"
                DebugLogger.log(error_msg, level='ERROR')
                return error_msg
        error_msg = 'Function not found.'
        DebugLogger.log(error_msg, level='WARNING')
        return error_msg

class ChatAssistant:
    def __init__(self, model='gpt-4o-mini', max_tokens=4096, user_id='default_user'):
        self.model = model
        self.max_tokens = max_tokens
        self.user_id = user_id
        st.session_state.messages = self.load_chat_history()

    def load_chat_history(self):
        history_file = os.path.join(CHAT_HISTORY_PATH, f"{self.user_id}.json")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                DebugLogger.log("Loaded existing chat history.", level='SYSTEM')
                return json.load(f)
        else:
            DebugLogger.log("No existing history found. Initializing with system prompt.", level='SYSTEM')
            return SYSTEM_PROMPT.copy()

    def save_chat_history(self):
        if not os.path.exists(CHAT_HISTORY_PATH):
            os.makedirs(CHAT_HISTORY_PATH)
        with open(os.path.join(CHAT_HISTORY_PATH, f"{self.user_id}.json"), 'w') as f:
            json.dump(st.session_state.messages, f)

    def chat_completion_request(self, chat_history, functions_data=None, function_call=None):
        DebugLogger.log("Sending request to chat completion API", level='SYSTEM')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ.get('OPENAI_API_KEY')
        }
        json_data = {
            'model': self.model,
            'messages': chat_history,
            'max_tokens': self.max_tokens,
            'functions': functions_data
        }
        if function_call is not None:
            json_data.update({'function_call': function_call})
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=json_data
            )
            response_data = response.json()
            DebugLogger.log(f"API response: {response_data}", level='API')
            return response_data
        except requests.exceptions.RequestException as e:
            DebugLogger.log(f"Request exception: {e}", level='ERROR')
            return None

    def run(self):
        functions_data = FunctionLoader.load_functions_from_json("functions.json")
        DebugLogger.log("Displaying initial conversation history", level='SYSTEM')
        st.title('GPT-4o Assistant')
        for msg in st.session_state.messages:
            if msg['role'] != 'function':
                with st.chat_message(msg['role']):
                    st.markdown(msg['content'])

        if prompt := st.chat_input('Enter user message...'):
            DebugLogger.log(f"Received user input: {prompt}", level='SYSTEM')
            st.chat_message('user').markdown(prompt)
            st.session_state.messages.append({'role': 'user', 'content': prompt})

            response = self.chat_completion_request(
                st.session_state.messages,
                functions_data=functions_data
            )
            assistant_message = response["choices"][0]["message"]
            DebugLogger.log(f"Assistant response: {assistant_message}", level='SYSTEM')

            while "function_call" in assistant_message:
                st.session_state.messages.append(assistant_message)
                function_name = assistant_message["function_call"]["name"]
                function_args = json.loads(assistant_message["function_call"]["arguments"])
                result = FunctionExecutor.execute_function(function_name, function_args)
                st.session_state.messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": str(result)
                })

                response = self.chat_completion_request(
                    st.session_state.messages,
                    functions_data=functions_data
                )

                assistant_message = response["choices"][0]["message"]

            if not st.session_state.messages[-1]["content"] == assistant_message['content']:
                st.chat_message('assistant').markdown(assistant_message['content'])
                st.session_state.messages.append(assistant_message)

            self.save_chat_history()

assistant = ChatAssistant(user_id='user')
assistant.run()