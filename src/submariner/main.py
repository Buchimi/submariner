import typer
from submariner.env import Env
from langchain.chat_models import init_chat_model
from rich import print
from submariner.customtypes.crashcourse import CrashCourse
import importlib
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Group
from submariner.interfaces.module import Module, Entity
from submariner.interfaces.virtualenv import NewVirtualEnvironment
from submariner.customtypes.response import AIResponse, Explanation
from submariner.checks import Checks

app = typer.Typer()
Env()
new_model = init_chat_model(model="gemini-2.0-flash", model_provider="google_genai")

console : Console = Console()

def gen_deepdive_answer(module: Entity):
    def print_ai_response(response: AIResponse):
        # classes 
        units: list[list[Explanation]] = [response.classes, response.functions, response.subpackages]
        names: list[str] = ["Classes", "Functions", "Subpackages"]
        summary = []
        for funcs, name in zip(units, names):
            aggregation = []
            if not funcs:
                continue
            for func in funcs:
                
                # can either be a class, function or subpackage
                code_examples = []
                for example in func.examples:
                    code_examples.append(Panel(f"```{example.code}```", title="Code Example"))
                examples_group = Group(*code_examples)
                aggregation.append(
                    Group(
                        Markdown(f"## {func.name}\n {func.use}"),
                        examples_group,
                    )
                )
            summary.append(Panel(Group(*aggregation), title=name))

        print(Group(*summary))
        
    prompt = module.prompt()
    model_with_structured_output = new_model.with_structured_output(AIResponse)
    result: AIResponse = model_with_structured_output.invoke(prompt)
    # Print

    print_ai_response(result)

def spark(python_module:str):
    """
    Gen a crashcourse.
    """
    raise NotImplementedError("Not implemented yet")
    # ai.run_main(generate_answer(CrashCourse.prompt(python_module)))

@app.command()
def status():
    """
    Check if the app can run with no problems.
    """
    check_runner = Checks()
    check_runner.check()
    ...
@app.command()
def deepdive(module_str:str, use_ai: bool = False, goal: str | None = None,):
    """
    Describe a function or class in a python module and how it could be used.
    """ 
    # try to import the module
    module_str_split = module_str.split(".")
    start = 0
    # create the virtual environment
    virtual_env = NewVirtualEnvironment(module_str_split[start])
    virtual_env.enter_env()
    module: Entity = Module(module_str_split[start])
    start = 1
    while start < len(module_str_split):
        module_str = module_str_split[start]
        if isinstance(module, Module):
            module = module.resolve_attribute(module_str)
        else:
            break
        start +=1
    
    if use_ai:
        gen_deepdive_answer(module)
    else:
        #TODO: rename
        module.pretty_print()

def main():
    app()

if __name__ == "__main__":
    main()
