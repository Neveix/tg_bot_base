from telegram import Bot

class BotManager:
    def __init__(self):
        from . import CommandManager
        self.command_manager = CommandManager(self)
        from . import CallbackQueryManager
        self.callback_query_manager = CallbackQueryManager(self)
        from . import UserLocalData
        self.user_local_data = UserLocalData(self)
        from . import UserGlobalData
        self.user_global_data: UserGlobalData = None
        from . import MessageManager
        self.message_manager = MessageManager(self)
        self.bot = None
        from . import ScreenManager
        self.screen_manager = ScreenManager(self)
        from . import UserScreenManager
        self.user_screen_manager = UserScreenManager
    def set_bot(self, bot: Bot):
        self.bot = bot