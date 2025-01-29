from .bot_manager import BotManager
from .callback_data import CallbackData

class CallbackQueryManager:
    """
Класс обеспечивает работу обработчика колбэков нажатия на кнопки.
"""
    def __init__(self, bot_manager: BotManager):
        self.bot_manager: BotManager = bot_manager
        async def callback_query_handler(query_data: str, user_id: int, **kwargs):
            callback_data = self.bot_manager.user_data_manager.get(user_id).callback_data
            if not callback_data:
                return
            if query_data not in callback_data:
                return
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
                for kwarg in kwargs:
                    if kwarg in data.kwargs:
                        raise ValueError(
f"FunctionCallbackData kwarg '{kwarg}' intersects with CallbackQueryHandler's kwarg.\
Please change the name of your kwarg.")
                await function(bot_manager=self.bot_manager,
                    **kwargs, user_id=user_id, *data.args[1:], **data.kwargs)
            elif data.action == "url":
                url = data.kwargs["url"]
        self.callback_query_handler = callback_query_handler
    def get_handler(self): ...