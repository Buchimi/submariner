import typer
from env import Env
from genkit.ai import Genkit
from genkit.plugins.google_genai import GoogleAI
from rich import print
from customtypes.crashcourse import CrashCourse

app = typer.Typer()
Env()
ai = Genkit(plugins=[GoogleAI()], model="googleai/gemini-2.0-flash")
     
async def generate_answer(prompt:str) :
    result = await ai.generate(prompt=prompt, output_schema=CrashCourse)
    cc: CrashCourse =  CrashCourse.model_validate(result.output)
    cc.print()
    cc.printCodeBlocks()
    
@app.command()
def crashcourse(python_module:str):
    """
    Gen a crashcourse.
    """
    # try:
    #     module = importlib.import_module(python_module)
    #     print(module.__doc__)
    # except ImportError:
    #     print(f"Module '{python_module}' not found.")
    ai.run_main(generate_answer(CrashCourse.prompt(python_module)))
    
        

if __name__ == "__main__":
    
    app()