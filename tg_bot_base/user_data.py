from typing import TYPE_CHECKING, Any, Callable, Coroutine

from telegram import Update, Message
from telegram.ext import CallbackContext
if TYPE_CHECKING:
    from .bot_manager import BotManager

class UserData:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.callback_data: list[str] = []
        self.media_group_id: str = None
        self.after_input: Callable[[Message, BotManager, int, Update, CallbackContext], Coroutine[Any, Any, None]] = None
        self.directory_stack: list[str] = []
        from .evaluated_screen import EvaluatedScreen
        self.screen: EvaluatedScreen = None

class UserDataManager:
    def __init__(self, bot_manager: "BotManager"):
        self.bot_manager = bot_manager
        self.user_data_type = UserData``
        self.__users_data: dict[str, UserData] = {}
    def get(self, user_id: int) -> UserData:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = self.user_data_type(user_id)
            self.__users_data[user_id] = user_data
        return user_data
    def reset(self, user_id: int) -> None:
        user_data = self.user_data_type(user_id)
        self.__users_data[user_id] = user_data
        
