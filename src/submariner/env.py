from dotenv import load_dotenv
import os

class Env:
    def __init__(self):
        load_dotenv()

    def get(self, key: str) -> str | None:
        return os.getenv(key)

def is_debug_mode() -> bool:
    return bool(os.getenv("SUBMARINER_DEBUG", False))

def is_dev_mode() -> bool:
    return not is_debug_mode()
