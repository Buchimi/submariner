import typer
from .env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from langchain.chat_models import init_chat_model
from rich import print
from .customtypes.crashcourse import CrashCourse
import importlib
from rich.console import Console
from .interfaces.module import Module
from .interfaces.virtualenv import NewVirtualEnvironment

app = typer.Typer()
Env()
ai = Genkit(plugins=[GoogleAI()], model="googleai/gemini-2.0-flash")
new_model = init_chat_model(model="gemini-2.0-flash", model_provider="google_genai")

console : Console = Console()

async def generate_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, output_schema=CrashCourse)
    cc: CrashCourse =  CrashCourse.model_validate(result.output)
    cc.printCodeBlocks()

async def generate_deepdive_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, )
    print(result.text)

def gen_deepdive_answer(prompt:str):
    result = new_model.invoke(prompt).content
    print(result)

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
    # create the virtual environment
    virtual_env = NewVirtualEnvironment(module_str_split[start])
    virtual_env.enter_env()
    module = Module(module_str_split[start])
    start = 1
    while start < len(module_str_split):
        module_str = module_str_split[start]
        module = module.resolve_attribute(module_str)
        if not isinstance(module, Module):
            break
        start +=1

    if use_ai:
        gen_deepdive_answer(module.prompt(goal))
    else:
        module.pretty_print()

def main():
    app()

if __name__ == "__main__":
    main()
