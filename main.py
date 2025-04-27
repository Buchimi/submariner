import typer
import importlib
from env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from pydantic import BaseModel, Field
from typing import Type, Any
from customtypes.keypoint import KeyPoint
from rich import print
from rich.panel import Panel

app = typer.Typer()
Env()
ai = Genkit(plugins=[GoogleAI()], model="googleai/gemini-2.0-flash")

class CrashCourse(BaseModel):
    title :str = Field(description="A very simple, very brief title of the crash course. ")
    keypoints: list[str] = Field(description="A list of keypoints to get up and running. ")

    @staticmethod
    def prompt(module:str):
        return f"Generate a crash course for how to use python module:{module}. Go over the basics to get up and running quickly.In your keypoints, favor writing succint keypoints (3-4) and favor adding code and terminal commands"

    def __str__(self):
        return f"""
        Keypoints: {self.keypoints} 
        """
    
    def print(self):
        panel = Panel(str(self), title=self.title)
        print(panel)
        
async def generate_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, output_schema=CrashCourse)
    cc: CrashCourse =  CrashCourse.model_validate(result.output)
    cc.print()
    


@app.command()
def crashcourse(python_module:str):
    """
    Dynamically import a Python module and print its docstring.
    """
    try:
        module = importlib.import_module(python_module)
        print(module.__doc__)
    except ImportError:
        print(f"Module '{python_module}' not found.")
    ai.run_main(generate_answer(CrashCourse.prompt(python_module)))
    
        

if __name__ == "__main__":
    
    app()