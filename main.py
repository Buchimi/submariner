import typer
from typing import Literal

app = typer.Typer()

@app.command()
def crashcourse(python_module:str):
    print("yo")

    
if __name__ == "__main__":
    app()