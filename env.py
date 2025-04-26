import os
class Env:
    def __init__():
        environment = os.environ
        self.openai_apikey = os.environ.get("OPENAI_API_KEY")
        if not self.openai_apikey:
            raise Exception("idk")