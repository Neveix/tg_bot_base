from method import Method

class MethodManager:
    __method__dict__: dict[str, Method]
    def __init__(self, bot):
        self.bot = bot
        self.__method__dict__ = {}
    def add(self, method: Method):
        method.method_manager = self
        self.__method__dict__[method.name] = method
    def get(self, name: str) -> Method:
        return self.__method__dict__[name]