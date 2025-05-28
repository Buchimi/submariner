from pydantic import BaseModel, Field
class Explanation(BaseModel):
    type : str = Field(description="Whether this is a function, class or a subpackage")
    use : str = Field(description="What this is used for.")
    how_to_use: str | None = Field(default=None, description="An example of how this is used. Not required.")

class AIResponse(BaseModel):
    functions : list[Explanation] = Field(description="A list of revelant functions that the AI responds with")
    classes: list[Explanation] = Field(description="A list of relevant classes and what they are for")
    subpackages: list[Explanation] = Field(description="A list of subpackages and their use")