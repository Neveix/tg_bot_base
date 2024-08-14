class BotManager:
    def __init__(self):
        from .operation_manager import OperationManager
        from .command_manager import CommandManager
        from .method_manager import MethodManager
        from .button_manager import ButtonManager
        from .user_local_data import UserLocalData
        
        self.operation_manager = OperationManager(self)
        self.command_manager = CommandManager(self)
        self.method_manager = MethodManager(self)
        self.button_manager = ButtonManager(self)
        self.user_local_data = UserLocalData(self)