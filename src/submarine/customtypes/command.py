from pydantic import BaseModel, Field
class TerminalCommand(BaseModel):
    command :str = Field(description="A single command strip")