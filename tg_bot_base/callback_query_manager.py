from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram import Update
from .bot_manager import BotManager
from .callback_data import CallbackData

class CallbackQueryManager:
    """
Класс обеспечивает работу обработчика колбэков нажатия на кнопки.
"""
    def __init__(self, bot_manager: BotManager):
        self.bot_manager: BotManager = bot_manager
        async def callback_query_handler(update: Update, context: CallbackContext):
            query = update.callback_query
            user_id: int = query.from_user.id
            await query.answer()
            callback_data = self.bot_manager.user_data_manager.get(user_id).callback_data
            if not callback_data:
                return
            if len(callback_data) <= int(query.data):
                return
            data: CallbackData = callback_data[int(query.data)]
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
                await function(bot_manager=self.bot_manager,
                    update=update, context=context, user_id=user_id, *data.args[1:], **data.kwargs)
                await update.callback_query.answer()
            elif data.action == "url":
                url = data.kwargs["url"]
        self.callback_query_handler = callback_query_handler
    def get_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.callback_query_handler)