from .DebugLogger import DebugLogger
from .CommandExecutor import CommandExecutor
from .WebSearcher import WebSearcher
import streamlit as st

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