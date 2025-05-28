from pydantic import BaseModel, Field
class AIResponse(BaseModel):
    functions : list[str] = Field(description="A list of revelant functions that the AI responds with")
    classes: list[str] = Field(description="A list of relevant classes and what they are for")
    subpackages: list[str] = Field(description="A list of subpackages and their use")