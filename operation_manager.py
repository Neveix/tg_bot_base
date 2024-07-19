from .operation import Operation

class OperationManager:
    __operation_dict__ : dict[str, Operation]
    def __init__(self, bot):
        self.bot = bot
        self.__operation_dict__ = {}
    def add(self, operation: Operation):
        operation.operation_manager = self
        self.__operation_dict__[operation.name] = operation
    def get(self, name: str):
        return self.__operation_dict__.get(name)
