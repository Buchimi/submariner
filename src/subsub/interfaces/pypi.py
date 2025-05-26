import requests
class PyPi:
    def __init__(self, module:str):
        if "." in module:
            self.module = module.split(".")[0]
        else:
            self.module = module
    
    def has_module(self) -> bool:
        url = f"https://pypi.org/pypi/{self.module}/json"
        response = requests.get(url)
        return response.status_code == 200
        