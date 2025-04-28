import os
import sys
from pathlib import Path
import venv

class VirtualEnvironment:
    auto_venv = ".venv"
    def __init__(self, ):
        """
        Creates a virtual environment if one isn't created yet. 
        Also links to a virtual env.
        """
        current_dir = Path(os.getcwd())
        venv_dir = current_dir.joinpath(self.auto_venv)
        if VirtualEnvironment.is_venv(venv_dir):
            ...
        else:
            venv.create(venv_dir, with_pip=True)
        self.venv_dir = venv_dir
    
    def enter_env(self):
        """
        Checks if the program is currently running in a virtual envrionment. 
        If it is not, it instead reruns the program in a virtual envrironment.
        """
        if not VirtualEnvironment.is_in_venv():
            python_path = self.venv_dir / "bin" / "python3"
            if not os.path.isfile(python_path):
                python_path = self.venv_dir / 'Scripts' / 'python.exe'
            if not os.path.isfile(python_path):
                raise FileNotFoundError("Could not find Python executable in the virtual environment.")
            print("Entering virtual environment, will rerun tool")
            os.execv(python_path, [python_path] + sys.argv)

    @staticmethod
    def is_in_venv():
        return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    @staticmethod
    def is_venv(path : Path):
        return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, 'pyvenv.cfg'))
    )


if __name__ == "__main__":
    virtualenv = VirtualEnvironment()
    
    virtualenv.enter_env()