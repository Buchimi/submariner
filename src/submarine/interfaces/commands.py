import abc
from abc import ABC, abstractmethod
import subprocess

class Command(ABC):
    @abstractmethod
    def get_command(self) -> list[str]:
        ...
    
    def get_command_run_log(self) -> str:
        return f"ran command {self.__class__.__name__}"

class CommandRunner:
    """
    Interface for running sub commands.
    Does not automatically run the command in a virtual environment."""
    def run_command(self, command:Command, suppress_output:bool = False):
        subprocess.check_call(command.get_command(), stdout=subprocess.DEVNULL if suppress_output else None)
        print(command.get_command_run_log())

class PipInstall(Command):
    def __init__(self, module):
        self.module = module
        
    def get_command(self) -> list[str]:
        return ["pip", "install", self.module]
    def get_command_run_log(self) -> str:
        return f"Pip installed {self.module}"
    
class InstallSubmarineDebug(Command):
    def __init__(self, python_path):
        self.python = python_path
    
    def get_command(self):
        return [self.python, "-m", "pip", "install", "."]

