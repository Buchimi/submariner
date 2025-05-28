from pydantic import BaseModel, Field
from typing import Literal

class Example(BaseModel):
    """A type for storing examples of how code items are used in specific packages. Only python code"""
    code : str = Field(description="A code snippet.")
class Explanation(BaseModel):
    type : Literal["function", "class", "subpackage"] = Field(description="Whether this is a function, class or a subpackage")
    name: str = Field(description="The name of what you are explaining")
    use : str = Field(description="What this is used for.")
    examples: list[Example] = Field(default=[], description="Some examples of how this is used. Not required but add about 2-3 examples where relevant. AI Instruction: Minimize on detail, about 2-5 lines. ")

class AIResponse(BaseModel):
    functions : list[Explanation] = Field(description="A list of revelant functions that the AI responds with")
    classes: list[Explanation] = Field(description="A list of relevant classes and what they are for")
    subpackages: list[Explanation] = Field(description="A list of subpackages and their use")