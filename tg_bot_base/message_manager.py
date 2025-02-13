from typing import Callable, TYPE_CHECKING
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler
if TYPE_CHECKING:
    from .bot_manager import BotManager

class MessageManager:
    def __init__(self, bot_manager: "BotManager"):
        self.bot_manager: "BotManager" = bot_manager
        
        async def handle_message(user_id: int, **kwargs):
            user_data = bot_manager.user_data_manager.get(user_id)
            
            # Очищаем экран
            bot_manager.user_screen_manager.clear_user_screen(user_id)
            
            # Получаем функцию, которую нужно вызвать после сообщения
            after_input = user_data.after_input
            if after_input is not None:
                # Удалем её из данных пользователя
                user_data.after_input = None
                # Вызываем её
                await after_input(bot_manager=bot_manager, user_id=user_id, **kwargs)
            
        self.handle_message = handle_message
    
    async def get_message_and_run_method(self, user_id: int, function: Callable):
        user_data = self.bot_manager.user_data_manager.get(user_id)
        user_data.after_input = function
    
    def get_handler(self):
        return MessageHandler(None, self.handle_message)