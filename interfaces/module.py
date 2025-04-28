import importlib
from .commands import PipInstall, CommandRunner
from .pypi import PyPi
from rich.console import Console
from types import ModuleType, FunctionType
from typing import Type

console = Console()

class Module:
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
        submodules =  [getattr(self.module, item) for item in all_attributes if isinstance(getattr(self.module, item), ModuleType)]
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
    
    
    

    
