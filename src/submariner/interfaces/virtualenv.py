import os
import sys
from pathlib import Path
import venv
from submariner.interfaces.commands import CommandRunner, InstallSubmariner, PipList
import re
from submariner.env import is_debug_mode

def is_in_venv():
    return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def is_venv(path : Path):
    return (
    os.path.isdir(path) and
    os.path.isfile(os.path.join(path, 'pyvenv.cfg'))
)

def get_env_path():
    return sys.prefix

class NewVirtualEnvironment:
    def __init__(self, package_name: str) -> None:
        # Make root dir
        base_path = os.path.expanduser("~/.submarine")
        os.makedirs(base_path, exist_ok=True)
        # resolve the name of the target dir
        target_path = Path(base_path) / package_name
        if not os.path.exists(target_path):
            # create target environment
            self.venv = venv.EnvBuilder(system_site_packages=False, with_pip=True)
            self.venv.create(target_path)

        self.location = base_path
        self.python = target_path / "bin" / "python"
        self.target_path = target_path
        if not os.path.isfile(self.python):
            self.python = target_path / 'Scripts' / 'python.exe'
        # self.pip = target_path / "bin" / "pip"
        # if not os.path.isfile(self.pip):
        #     self.pip = target_path / 'Scripts' / 'pip.exe'

        # install submariner conditionally
        if not self.has_submariner_installed() or is_debug_mode():
            self.install_submariner()

    
    def enter_env(self):
        if not is_in_venv() or not get_env_path().startswith(self.location):
            #create
            print("Entering virtual environment, will rerun tool")
            os.execv(self.python, [self.python] + sys.argv)
        else:
            print(f"Running in virtual environment at {self.target_path}")
    
    def has_submariner_installed(self) -> bool:
        cmd_runner = CommandRunner()
        result = cmd_runner.run_command(PipList(self.python))
        return bool(re.compile(r'submariner').findall(result))
        
    def install_submariner(self) -> None:
        cmd_runner = CommandRunner()
        cmd_runner.run_command(InstallSubmariner(self.python))

if __name__ == "__main__":

    virtualenv = VirtualEnvironment()
    
    virtualenv.enter_env()