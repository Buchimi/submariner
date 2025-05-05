import importlib
from .commands import PipInstall, CommandRunner
from .pypi import PyPi
from rich.console import Console
from types import ModuleType, FunctionType
from typing import Type
import inspect

console = Console()
class Promptable:
    def prompt(self, goal: str | None = None) -> str:
        raise NotImplementedError("prompt not implemented")
    
    @staticmethod
    def to_promptable(obj:object) -> "Promptable":
        """
        This will convert a object to one of the promptable subtypes.
        TODO: See if this function should be in the promptable class or as a member function of this module
        """
        if isinstance(obj, Promptable):
            return obj
        elif isinstance(obj, FunctionType):
            return Function(obj)
        elif isinstance(obj, ModuleType):
            return Module._from_module(obj)
        elif isinstance(obj, Type):
            raise NotImplementedError("Classes are not yet supported")
        else:
            raise TypeError(f"Entity {obj} is not a module, function or class")

class Function(Promptable):
    def __init__(self, function:FunctionType) -> None:
        self.function = function
        self.name = function.__name__
        self.args = inspect.signature(function).parameters
        self.docstring = function.__doc__
        self.module = Module(function.__module__)

    def __str__(self) -> str:
        return f"{self.name}({self.args})"
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
    
    def __repr__(self):
        return self.__str__()

    def __doc__(self) -> str:
        return self.docstring
    
class Module(Promptable):
    def __init__(self, module:str) -> None:
        try:
            self.module = importlib.import_module(module)
        except ModuleNotFoundError:
            # Do some rearranging
            fully_qualified_module_name = module
            module_split = module.split(".")
            index = 0
            module = module_split[index]

            # now instead of a module like os.path, it's just os
            if PyPi(module).has_module():
                console.log("Pypi has this module")
                clirunner = CommandRunner()
                clirunner.run_command(PipInstall(module))
                self.module = importlib.import_module(module)
                console.log("Module imported")
            else:
                # Genai fallback
                raise NotImplementedError(f"Module {module} not found")
        
    @classmethod
    def _from_module(cls, module:ModuleType):
        if not isinstance(module, ModuleType):
            raise TypeError("module must be a ModuleType")
        mod = object.__new__(cls)
        mod.module = module
        return mod

    def _get_all_attributes(self) -> list[str]:
        return list(filter( lambda item: (not item.startswith("__")), dir(self.module)))
        
    def submodules(self) -> list[ModuleType]:
        all_attributes = self._get_all_attributes()
        submodules =  [getattr(self.module, item) for item in all_attributes if isinstance(getattr(self.module, item), ModuleType) and getattr(getattr(self.module, item), "__name__").startswith(self.module.__name__)]
        return [Module._from_module(mod) for mod in submodules]
    
    def get_submodule(self, module_name:str) -> ModuleType:
        """
        Simply gets a submodule.
        Consider support for fuzzy search
        """
        if hasattr(self.module, module_name):
            mod = getattr(self.module, module_name)
            if not isinstance(mod, ModuleType):
                raise TypeError(f"Module {module_name} is not a module")
            return Module._from_module(mod)
        else:
            raise ValueError(f"Module {module_name} not found")
    
    def resolve_attribute(self, attr:str) -> Promptable:
        if hasattr(self.module, attr):
            entity = getattr(self.module, attr)
            return Promptable.to_promptable(entity)
        else:
            members = self.members()
            for member in members:
                if hasattr(member, attr):
                    return Promptable.to_promptable(getattr(member, attr))
            raise ValueError(f"Entity {attr} not found")

    def classes(self) -> list[Type]:
        all_attributes = self._get_all_attributes()
        classes =  [getattr(self.module, item) for item in all_attributes if isinstance(getattr(self.module, item), type)]
        return classes
    
    def functions(self) -> list[Function]:
        all_attributes = self._get_all_attributes()
        functions =  [Function(getattr(self.module, item)) for item in all_attributes if isinstance(getattr(self.module, item), FunctionType)]
        return functions
    
    def members(self):
        return self.functions() + self.classes()
    
    def __str__(self) -> str:
        return f"Module: {self.module.__name__}" + "\n"+ f"{self.module.__doc__.splitlines()[0] if self.module.__doc__ else ''}"
    def __doc__(self) -> str:
        return self.module.__doc__ if self.module.__doc__ else str(self.module)
    
    def __repr__(self) -> str:
        return self.__str__()

    def prompt(self, goal: str | None = None, be_brief:bool = True) -> str:
        prompt_builder = []
        if goal:
            prompt_builder.append(f"""Tell me how the python module: {str(self.module)} could be used to achieve the goal: {goal}""")
        else:

            prompt_builder.append(f"""Explain the use of the python module: {str(self.module)}. What it's for and what members I am likely to use""")
        if be_brief:
            prompt_builder.append("Be very brief in your analysis, as though you were a cli tool or a programmer with a short attention span")
        
        return "\n".join(prompt_builder)