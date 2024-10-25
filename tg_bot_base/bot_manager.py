from telegram import Bot

class BotManager:
    def __init__(self):
        from . import CommandManager
        self.command_manager = CommandManager(self)
        from . import CallbackQueryManager
        self.callback_query_manager = CallbackQueryManager(self)
        from . import UserDataManager
        self.user_data_manager = UserDataManager(self)
        from . import MessageManager
        self.message_manager = MessageManager(self)
        from . import ScreenManager
        self.screen_manager = ScreenManager(self)
        from . import UserScreenManager
        self.user_screen_manager = UserScreenManager(self)
        from . import TelegramInterface
        self.telegram_interface = TelegramInterface(self)
        self.bot: Bot | None = None
    def set_bot(self, bot: Bot):
        self.bot = bot