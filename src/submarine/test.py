import os
from dotenv import load_dotenv
import sys
from pathlib import Path
import venv



class VirtualEnvironment:
    auto_venv = ".auto_venv"
    def __init__(self, ):
        current_dir = os.getcwd()
        path = Path(current_dir)
        venv_dir = path.joinpath(self.auto_venv)
        venv.create(venv_dir, with_pip=True)
        
        
        ...
    
    @staticmethod
    def is_in_venv():
        return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

    
    
    

