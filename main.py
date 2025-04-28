import typer
from env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from rich import print
from customtypes.crashcourse import CrashCourse
import importlib
from pypi import PyPi
from rich.console import Console
from commands import CommandRunner, PipInstall

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
        # Do some rearranging
        fully_qualified_module_name = module
        module_split = module.split(".")
        module = module_split[0]

        # now instead of a module like os.path, it's just os
        if PyPi(module).has_module():
            console.log("Pypi has this module")
            clirunner = CommandRunner()
            clirunner.run_command(PipInstall(module))
            module = importlib.import_module(module)
            console.log("Module imported")
            print(module)

        else:
            # Genai fallback
            raise NotImplementedError(f"Module {module} not found")
            


if __name__ == "__main__":
    app()