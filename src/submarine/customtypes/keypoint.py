from pydantic import BaseModel, Field
from .codeblock import CodeBlock
from .command import TerminalCommand
from typing import Union

class KeyPoint(BaseModel):
    summary : str = Field(description="A summary of this key point")
    snippet: str = Field(description="Either a terminal command or code snippet")