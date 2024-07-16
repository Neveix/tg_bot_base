from operation_manager import OperationManager
from command_manager import CommandManager

class BotManager:
    def __init__(self):
        self.operation_manager = OperationManager(self)