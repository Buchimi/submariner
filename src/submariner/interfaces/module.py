import importlib
from submariner.interfaces.commands import PipInstall, CommandRunner
from submariner.interfaces.pypi import PyPi
from submariner.interfaces.virtualenv import NewVirtualEnvironment
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from types import ModuleType, FunctionType
from typing import Type
import inspect
from abc import abstractmethod, ABC


console = Console()
class Entity(ABC):
    @abstractmethod
    def prompt(self, goal: str | None = None, be_brief:bool = True) -> str:
        raise NotImplementedError("prompt not implemented")
    
    def _get_all_attributes(self, root) -> list[str]:
        return list(filter( lambda item: (not item.startswith("__")), dir(root)))

    def pretty_print(self):
        raise NotImplementedError("pretty_print not implemented")
    
    @staticmethod
    def to_entity(obj:object) -> "Entity":
        """
        This will convert a object to one of the entity subtypes.
        TODO: See if this function should be in the entity class or as a member function of this module
        """
        if isinstance(obj, Entity):
            return obj
        elif isinstance(obj, FunctionType):
            return Function(obj)
        elif isinstance(obj, ModuleType):
            return Module._from_module(obj)
        elif isinstance(obj, Type):
            return Class(obj)
        else:
            raise TypeError(f"Entity {obj} is not a module, function or class")

class Function(Entity):
    def __init__(self, function:FunctionType) -> None:
        self.function = function
        self.name = function.__name__
        self.args = inspect.signature(function)
        self.docstring = function.__doc__
        self.module = Module(function.__module__)

    def __str__(self) -> str:
        return f"{self.name}{self.args}"
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
    
    def __repr__(self):
        return self.__str__()

    def __doc__(self) -> str:
        return self.docstring
    
    def prompt(self, goal: str | None = None, be_brief:bool = True) -> str:
        prompt_builder = []
        prompt_builder.append(f"Explain this python function to me. Include examples of how to use it")
        prompt_builder.append(f"The function is {str(self)} and it is found in {self.module}.")
        prompt_builder.append(f"Use it's docstring {self.docstring} as guidance")
        return "\n".join(prompt_builder)
    def pretty_print(self):
        functions = Panel(f"{self.name}:{self.args}",title="Signature")
        console.print(functions)
        
class Class(Entity):
    def __init__(self, cls:Type) -> None:
        self.cls = cls
        self.name = cls.__name__
        self.docstring = cls.__doc__
        self.module = cls.__module__

    def __str__(self) -> str:
        return f"{self.name}: {self.docstring.splitlines()[0] if self.docstring else 'No Docs'}"
    
    def __repr__(self):
        return self.__str__()

    def __doc__(self) -> str:
        return self.docstring
    
    @property
    def args(self) -> str:
        try:
            return str(inspect.signature(self.cls))
        except Exception:
            return ''
    
    def functions(self) -> list[Function]:
        all_attributes = self._get_all_attributes(self.cls)
        functions =  [Function(getattr(self.cls, item)) for item in all_attributes if isinstance(getattr(self.cls, item), FunctionType)]
        functions = list(filter(lambda function: not function.name.startswith("_"), functions))
        return functions
    
    def properties(self) -> list[Function]:
        # Problem: it shows all properties, not just variables
        return self.cls.__dict__.keys()

    def pretty_print(self) -> str:
        title = Markdown(f"## {self.name}")
        title_description = Markdown(f"{self.docstring.splitlines()[0] if self.docstring else ''}\n")
        signature = Panel(f"{self.name}{self.args}", title="Signature") if self.args else ''
        functions = Panel(Markdown("\n".join([f"- {function}" for function in self.functions()])), title="Functions") if self.functions() else ''
        #attributes = Panel(Markdown("\n".join([f"- {attribute}" for attribute in self.properties()])), title="Attributes") if self.properties() else ''
        console.print(*[title, title_description, signature, functions, 
        #attributes
        ])
    
    def prompt(self, goal: str | None = None, be_brief:bool = True) -> str:
        prompt_builder = []
        prompt_builder.append(f"Explain this python class to me {str(self)}. Include examples of how to use it")
        prompt_builder.append(f"The args of the class's invocation call is {self.args}. The properties are {self.properties()}.")
        prompt_builder.append(f"The class is found in {self.module} and some of it's functions are {self.functions()}.")
        return "\n".join(prompt_builder)

class Module(Entity):
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
                python_path = NewVirtualEnvironment(module).python
                clirunner.run_command(PipInstall(module, python_path))
                self.module = importlib.import_module(module)
                console.log("Module imported")
            else:
                # TODO: Genai fallback
                raise NotImplementedError(f"Module {module} not found and doesn't exist on pypi. Make sure you are using the right name.")
        
    @classmethod
    def _from_module(cls, module:ModuleType):
        if not isinstance(module, ModuleType):
            raise TypeError("module must be a ModuleType")
        mod = object.__new__(cls)
        mod.module = module
        return mod

    # Gets a list of all submodules in the module. 
    def submodules(self) -> list[ModuleType]:
        all_attributes = self._get_all_attributes(self.module)
        submodules =  [getattr(self.module, item) for item in all_attributes if isinstance(getattr(self.module, item), ModuleType) and getattr(getattr(self.module, item), "__name__").startswith(self.module.__name__)]
        submodules = [sub for sub in submodules if not str(sub).split(".")[1].startswith("_")]
        return [Module._from_module(mod) for mod in submodules]
    
    # Gets a single module. May be deprecated
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
    
    # Gets an attribute, which is basically a local entity like a class, function or submodule
    def resolve_attribute(self, attr:str) -> Entity:
        if hasattr(self.module, attr):
            entity = getattr(self.module, attr)
            return Entity.to_entity(entity)
        else:
            members = self.members()
            for member in members:
                if hasattr(member, attr):
                    return Entity.to_entity(getattr(member, attr))
            raise ValueError(f"Entity {attr} not found")

    # List of classes in the module
    def classes(self) -> list[Type]:
        all_attributes = self._get_all_attributes(self.module)
        classes =  [getattr(self.module, item) for item in all_attributes if isinstance(getattr(self.module, item), type)]
        classes = list(filter(lambda cls: cls.__module__.startswith(self.module.__name__), classes))
        return [Class(cls) for cls in classes]
    
    # List of functions in the module
    def functions(self) -> list[Function]:
        all_attributes = self._get_all_attributes(self.module)
        functions =  [Function(getattr(self.module, item)) for item in all_attributes if isinstance(getattr(self.module, item), FunctionType)]
        return functions
    
    # Lists all functions and classes in the module
    def members(self):
        return self.functions() + self.classes()
    
    def __str__(self) -> str:
        return f"Module: {self.module.__name__}" + "\n"+ f"{self.module.__doc__.splitlines()[0] if self.module.__doc__ else ''}"
    def __doc__(self) -> str:
        return self.module.__doc__ if self.module.__doc__ else str(self.module)

    def __repr__(self) -> str:
        return self.__str__()
    
    def pretty_print(self):
        def panel_markdown_gen(list_of_entities: list[str], title: str) -> str:
            if not list_of_entities:
                return None
            return Panel(Markdown("\n".join([f"- {item}" for item in list_of_entities])), title=title)

        title = Markdown(f"## {self.module.__name__}\n")
        title_description = Markdown(f"{self.module.__doc__.splitlines()[0] if self.module.__doc__ else ''}\n")
        functions = panel_markdown_gen(self.functions(), "Functions")
        classes = panel_markdown_gen(self.classes(), "Classes")
        submodules = panel_markdown_gen(self.submodules(), "Submodules")
        print_order = [title, title_description, functions, classes, submodules]
        print_order = [item for item in print_order if item is not None]
        console.print(*print_order)


    def prompt(self, goal: str | None = None, be_brief:bool = True) -> str:
        prompt_builder = []
        if goal:
            prompt_builder.append(f"""Tell me how the python module: {str(self.module)} could be used to achieve the goal: {goal}""")
        else:
            prompt_builder.append(f"""Explain the use of the python module: {str(self.module)}. What it's for and what members I am likely to use""")
            prompt_builder.append(f"the functions are {str(self.functions())}")
            prompt_builder.append(f"the classes are {str(self.classes())}")
            prompt_builder.append(f"the submodules are {str(self.submodules())}")
        if be_brief:
            prompt_builder.append("Be very brief in your analysis, as though you were a cli tool or a programmer with a short attention span")
        
        return "\n".join(prompt_builder)