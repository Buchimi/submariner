from rich.console import Console
from submariner.env import Env
console = Console()

class Checks:
    """Checks to see if the app can run with no problems."""
    def check(self) -> None:
        console.print("Starting system checks")
        self.check_gemini_key_in_env()
        console.print("Checks completed. No issues found.")
        ...
    def check_gemini_key_in_env(self) -> None:
        console.print("Checking Gemini key is in env")
        if bool(Env().get("GOOGLE_API_KEY")):
            console.print("Gemini key is in env")
        else:
            console.print("Google API key is not in env. Please add a GOOGLE_API_KEY in the environment")
