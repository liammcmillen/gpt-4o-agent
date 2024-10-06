from .DebugLogger import DebugLogger
import json

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