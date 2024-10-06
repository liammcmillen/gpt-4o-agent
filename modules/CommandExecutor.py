import subprocess
from .DebugLogger import DebugLogger

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