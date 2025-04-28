import typer
from env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from rich import print
from customtypes.crashcourse import CrashCourse
import importlib
from pypi import PyPi
from rich.console import Console

app = typer.Typer()
Env()
ai = Genkit(plugins=[GoogleAI()], model="googleai/gemini-2.0-flash")
console : Console = Console()

async def generate_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, output_schema=CrashCourse)
    cc: CrashCourse =  CrashCourse.model_validate(result.output)
    cc.printCodeBlocks()
    
@app.command()
def spark(python_module:str):
    """
    Gen a crashcourse.
    """
    ai.run_main(generate_answer(CrashCourse.prompt(python_module)))
    
@app.command()
def deepdive(module:str):
    """
    Describe a function or class in a python module and how it could be used.
    """ 
    # try to import the module

    try:
        module = importlib.import_module(module)
    except ModuleNotFoundError:
        if PyPi(module).has_module():
            console.log("Pypi has this module")
            
        else:
            # Genai fallback
            raise NotImplementedError(f"Module {module} not found")
            


if __name__ == "__main__":
    app()