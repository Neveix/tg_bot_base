from typing import Callable, TYPE_CHECKING
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import Update
from .callback_data import CallbackData
if TYPE_CHECKING:
    from .bot_manager import BotManager

class CallbackQueryManager:
    """
Класс обеспечивает работу обработчика колбэков нажатия на кнопки.
"""
    def __init__(self, bot_manager: "BotManager"):
        self.dummy_handle_func: Callable[[Update, CallbackContext], None]
        self.bot_manager: "BotManager" = bot_manager
        
        async def callback_query_handler(user_id: int, query_data: str):
            callback_data = self.bot_manager.user_data_manager.get(user_id).callback_data
            data: CallbackData = callback_data[query_data]
            
            if data.action == "menu":
                screen_name: str = data.args[0]
                if not isinstance(screen_name, str):
                    raise ValueError(f"{screen_name=} is not str")
                await bot_manager.user_screen_manager.set_user_screen_by_name(user_id, screen_name)
            
            elif data.action == "step_back":
                await bot_manager.user_screen_manager.step_back(user_id)
            
            elif data.action == "function":
                function = data.args[0]
                if not callable(function):
                    raise ValueError("Callback data has no function")
                await function(*data.args[1:], bot_manager=self.bot_manager,
                    user_id=user_id, **data.kwargs)
        self.callback_query_handler = callback_query_handler
    def get_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.callback_query_handler)