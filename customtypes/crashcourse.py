import re
from dataclasses import dataclass
from pydantic import BaseModel, Field
from rich.panel import Panel
from rich.console import Group, Console
console = Console()

@dataclass
class LanguageCodePair:
    lang: str
    code: str

class CrashCourse(BaseModel):
    title :str = Field(description="A very simple, very brief title of the crash course. ")
    keypoints: list[str] = Field(description="A list of keypoints to get up and running. ")

    @staticmethod
    def prompt(module:str):
        return f"""Generate a crash course for how to use python module:{module}. Go over the basics to get up and running quickly.
        In your keypoints, favor writing succint keypoints (3-4) and favor adding code and terminal commands.
        Things to note:
        don't use single backticks (`) for code or terminal commands, only use triple backticks (```)
        You are primarily concerned about python packages"""

    def __str__(self):
        return f"""
        Keypoints: {self.keypoints} 
        """
    
    def print(self):
        panel = Panel(str(self), title=self.title)
        print(panel)
    
    def getCodeBlocks(self) -> LanguageCodePair:
        regex = r"```(\w+)\n(.+)```"
        codeblocks = []
        for keypoint in self.keypoints:
            matches = re.findall(regex, keypoint, re.DOTALL)
            for language, code in matches:
                pair = LanguageCodePair(language, code)
                codeblocks.append(pair)
        return codeblocks
    
    def printCodeBlocks(self) -> None:
        codeblocks : LanguageCodePair = self.getCodeBlocks()
        groups : Group = Group(*[Panel(codeblock.code, title=codeblock.lang) for codeblock in codeblocks])
        panel : Panel = Panel(groups, title="Code Blocks")
        console.print(panel)
   