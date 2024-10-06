from datetime import datetime

class DebugLogger:
    LEVEL_COLOR_SCHEME = {
        'INFO': '\033[94m',  # Blue
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'API': '\033[92m',  # Green
        'SYSTEM': '\033[95m'  # Purple
    }

    @staticmethod
    def log(message, level='INFO'):
        color = DebugLogger.LEVEL_COLOR_SCHEME.get(level, '\033[0m')
        reset_color = '\033[0m'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{level}] [{timestamp}] {message}{reset_color}")