from .command_manager import CommandManager
from .callback_query_manager import CallbackQueryManager
from .user_data import UserDataManager
from .message_manager import MessageManager
from .screen_manager import ScreenManager
from .user_screen_manager import UserScreenManager
from .telegram_interface import TelegramInterface


class BotManager:
    def __init__(self):
        self.command_manager = CommandManager(self)
        self.callback_query_manager = CallbackQueryManager(self)
        self.user_data_manager = UserDataManager(self)
        self.message_manager = MessageManager(self)
        self.screen_manager = ScreenManager(self)
        self.user_screen_manager = UserScreenManager(self)
        self.telegram_interface = TelegramInterface(self)
