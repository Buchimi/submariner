import abc
from abc import ABC, abstractmethod
import subprocess
from virtualenv import VirtualEnvironment

class Command(ABC):
    @abstractmethod
    def getCommand(self) -> list[str]:
        ...
    
    def getCommandRunLog(self) -> str:
        ...

class CommandRunner:
    def run_command(self, command:Command, run_in_env:bool=True):
        if run_in_env:
            venv = VirtualEnvironment()
            venv.enter_env()
        subprocess.check_call(command.getCommand())
        print(command.getCommandRunLog())

class PipInstall(Command):
    def __init__(self, module):
        self.module = module
        
    def getCommand(self) -> list[str]:
        return ["pip", "install", self.module]
    def getCommandRunLog(self) -> str:
        return f"Pip installed {self.module}"
    
    

