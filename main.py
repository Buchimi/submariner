import typer
from env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from rich import print
from customtypes.crashcourse import CrashCourse
import importlib
from rich.console import Console
from interfaces.module import Module

app = typer.Typer()
Env()
ai = Genkit(plugins=[GoogleAI()], model="googleai/gemini-2.0-flash")
console : Console = Console()

async def generate_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, output_schema=CrashCourse)
    cc: CrashCourse =  CrashCourse.model_validate(result.output)
    cc.printCodeBlocks()

async def generate_deepdive_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, )
    print(result.text)

@app.command()
def spark(python_module:str):
    """
    Gen a crashcourse.
    """
    ai.run_main(generate_answer(CrashCourse.prompt(python_module)))
    
@app.command()
def deepdive(module_str:str, use_ai: bool = False, goal: str | None = None):
    """
    Describe a function or class in a python module and how it could be used.
    """ 
    # try to import the module
    module_str_split = module_str.split(".")
    start = 0
    module = Module(module_str_split[start])
    start = 1
    while start < len(module_str_split):
        module_str = module_str_split[start]
        module = module.resolve_attribute(module_str)
        if not isinstance(module, Module):
            break
        start +=1
    
    if use_ai:
        ai.run_main(generate_deepdive_answer(module.prompt(goal)))
    else:
        if isinstance(module, Module):
            print(module)
            for member in module.members():
                print(member)
            print(module.submodules())
        else:
            print(module)

if __name__ == "__main__":
    app()