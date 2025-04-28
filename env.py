import os
from dotenv import load_dotenv
import sys
class Env:
    def __init__(self):
        load_dotenv()

def is_in_venv():
    return (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

class VirtualEnvironment:
    auto_venv = ".auto_venv"
    def __init__(self, ):
        ...
    
    
    

