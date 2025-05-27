import abc
from abc import ABC, abstractmethod
import subprocess

class Command(ABC):
    @abstractmethod
    def get_command(self) -> list[str]:
        ...
    
    def get_command_run_log(self) -> str:
        return f"ran command {self.__class__.__name__}"
    
    def get_pre_command_run_log(self) -> str:
        return f"running command {self.__class__.__name__}"

class CommandRunner:
    """
    Interface for running sub commands.
    Does not automatically run the command in a virtual environment."""
    def run_command(self, command:Command,) -> str:
        output = subprocess.check_output(command.get_command(), text=True)
        print(command.get_command_run_log())
        return output

class PipInstall(Command):
    def __init__(self, module, python_path):
        self.module = module
        self.python = python_path
        
    def get_command(self) -> list[str]:
        base_command = ["pip", "install", self.module]
        if self.python:
            return [self.python, "-m"] + base_command
        else:
            return base_command

    def get_command_run_log(self) -> str:
        return f"Pip installed {self.module}"

class PipList(Command):
    def __init__(self, python_path):
        self.python = python_path
    
    def get_command(self):
        return [self.python, "-m", "pip", "list"]

class InstallSubmarineDebug(Command):
    def __init__(self, python_path):
        self.python = python_path
    
    def get_command(self):
        return [self.python, "-m", "pip", "install", "."]
    
    def get_command_run_log(self) -> str:
        return f"Submariner debug installation successful."
    
    def get_pre_command_run_log(self) -> str:
        return f"Installing submariner debug at location {self.python}."


