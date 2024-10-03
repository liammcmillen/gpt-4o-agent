from helper_functions import *
import os
import pickle
import json
from colorama import Fore

system = [
    {
        "role": "system",
        "content": "You are a computer assistant on a Debian 12 linux machine with the capability to run bash commands. "
                   "Make sure to give descriptions of the steps that you are taking when executing commands and double check your work. "
                   "You should use all the tools and problem solving available to you to accomplish a task that was given to you. Be proactive!"
                   "Lastly, try to avoid running a command that you think would not end without manual input from the user."
    }
]

with open("functions.json", 'r') as file:
    functions = json.load(file)

class LLMAgent:
    def process_command(self, command):
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
