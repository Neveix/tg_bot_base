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
        
        async def callback_query_handler(update: Update, context: CallbackContext, **kwargs):
            query = update.callback_query
            user_id: int = query.from_user.id
            await query.answer()
            callback_data = self.bot_manager.user_data_manager.get(user_id).callback_data
            if not callback_data:
                await self.dummy_handle_func(update, context)
                return
            if query.data not in callback_data:
                await self.dummy_handle_func(update, context)
                return
            
            data: CallbackData = callback_data[query.data]
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
                for kwarg in kwargs:
                    if kwarg in data.kwargs:
                        raise ValueError(
f"FunctionCallbackData kwarg '{kwarg}' intersects with CallbackQueryHandler's kwarg.\
Please change the name of your kwarg.")
                await function(*data.args[1:], bot_manager=self.bot_manager,
                    **kwargs, user_id=user_id, **data.kwargs)
            elif data.action == "url":
                url = data.kwargs["url"]
        self.callback_query_handler = callback_query_handler
    def get_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.callback_query_handler)