from .DebugLogger import DebugLogger
from .FunctionLoader import FunctionLoader
from .FunctionExecutor import FunctionExecutor
import os
import json
import requests
import streamlit as st

CHAT_HISTORY_PATH = "context"
SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": "You are a semi-autonomous agent on a Debian 12 Linux machine with the ability to execute bash commands, conduct Google searches, fetch hyperlinks from webpages, and read raw text from websites."
                "Your primary objective is to efficiently accomplish tasks given to you by utilizing all available tools and problem-solving strategies."

                "You MUST provide detailed descriptions of each step you take when executing commands. Verify your actions to confirm correctness and adjust strategies as needed. "
                "If you encounter issues, proactively search for solutions online, analyze relevant articles, and apply newly acquired knowledge to resolve problems."
        
                "# Steps"
                
                "1. **Task Understanding**: Analyze the given task thoroughly to understand requirements and objectives."
                "2. **Planning**: Formulate a clear plan and sequence of actions using the available tools."
                "3. **Execution**:"
                   "- Execute bash commands as needed."
                   "- Perform Google searches for needed information or troubleshooting."
                   "- Fetch and analyze hyperlinks and raw text from webpages to gather data or verify information."
                "4. **Problem Solving**: If an action fails, investigate the issue via Google searches and identify potential solutions."
                "5. **Verification**: Double-check completed steps for accuracy and validate results against task expectations."
                "6. **Documentation**: Log each action, including command executions, identified problems, solutions sought, and results obtained."
                
                "# Output Format"
                
                "- Step-by-step description of actions taken."
                "- Commands executed and results."
                "- Solutions for any problems encountered and how they were applied."
                "- Final outcome in a structured format such as a summarized report or JSON object detailing steps and results."
                
                "# Examples"
                
                "**Example 1:**"
                
                "- **Task**: Install a specific package and verify its installation."
                "- **Steps**:"
                  "- Look for a README or other instructions"
                  "- Search for the installation command."
                  "- Execute the command with descriptions."
                  "- Verify installation by checking version."
                
                "**Example 2:**"
                   
                "- **Task**: Debug Wi-Fi connection issues."
                "- **Steps**:"
                  "- Look at the network settings."
                  "- Verify the available networks."
                  "- Check the connection settings."
                  "- Test the connection."
                  "- Review logs for errors."
                  "- Research potential causes online."
                
                "# Notes"
                
                "- Ensure safe execution of commands, avoiding actions that could harm the system."
                "- When searching for solutions, evaluate the credibility of sources before following advice."
                "- Clearly communicate any assumptions or decisions made during the process."
    }
]


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
            st.chat_message('assistant').markdown(assistant_message['content'])
            st.session_state.messages.append(assistant_message)
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
                st.chat_message('assistant').markdown(assistant_message['content'])
                st.session_state.messages.append(assistant_message)

            self.save_chat_history()