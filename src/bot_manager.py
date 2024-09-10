

class BotManager:
    def __init__(self):
        from .operation_manager import OperationManager
        self.operation_manager = OperationManager(self)
        from .command_manager import CommandManager
        self.command_manager = CommandManager(self)
        from .method_manager import MethodManager
        self.method_manager = MethodManager(self)
        from .button_manager import ButtonManager
        self.button_manager = ButtonManager(self)
        from .user_local_data import UserLocalData
        self.user_local_data = UserLocalData(self)