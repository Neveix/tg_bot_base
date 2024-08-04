from typing import Callable

class Method:
    def __init__(self, name: str, action: Callable):
        self.name = name
        self.action = action
        self.method_manager = None
    def run(self,**kwargs):
        self.action(**kwargs)