from pydantic import BaseModel, Field
class CodeBlock(BaseModel):
    code : list[str] = Field("Lines of code in the specified programming language. These lines should ideally be short, forming a snippet")