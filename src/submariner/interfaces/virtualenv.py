import os
import sys
from pathlib import Path
import venv
from .commands import CommandRunner, InstallSubmarineDebug

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
        if not os.path.isfile(self.python):
            self.python = target_path / 'Scripts' / 'python.exe'
        # self.pip = target_path / "bin" / "pip"
        # if not os.path.isfile(self.pip):
        #     self.pip = target_path / 'Scripts' / 'pip.exe'
    
    def enter_env(self):
        if not is_in_venv() or not get_env_path().startswith(self.location):
            # Install submarine. TODO: Conditional install
            cmd_runner = CommandRunner()
            cmd_runner.run_command(InstallSubmarineDebug(self.python))

            #create
            print("Entering virtual environment, will rerun tool")
            os.execv(self.python, [self.python] + sys.argv)
        else:
            print("Is already in virtual environment")
    
if __name__ == "__main__":

    virtualenv = VirtualEnvironment()
    
    virtualenv.enter_env()