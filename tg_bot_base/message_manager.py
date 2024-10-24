from typing import Callable
from telegram import Update
from telegram.ext import CallbackContext

class MessageManager:
    def __init__(self, bot_manager):
        from .bot_manager import BotManager
        self.bot_manager: BotManager = bot_manager
        async def handle_message(update: Update, context: CallbackContext):
            # Очищаем экран
            self.bot_manager.user_screen_manager.clear_user_screen(update.message.from_user.id)
            media_group_id = self.bot_manager.user_data_manager.get(
                update.message.from_user.id).media_group_id
            # Если у сообщения есть media
            if update.message.media_group_id is not None:
                # Если прошолое сообщение было с таким же media, выходим из функции
                if media_group_id == update.message.media_group_id:
                    return
                # Иначе - сохраняем media id.
                self.bot_manager.user_data_manager.get(
                    update.message.from_user.id).media_group_id = update.message.media_group_id
            # Получаем функцию, которую нужно вызвать после сообщения
            after_input = self.bot_manager.user_data_manager.get(
                update.message.from_user.id).after_input
            if after_input is not None:
                # Удалем её из данных пользователя
                self.bot_manager.user_data_manager.get(
                    update.message.from_user.id).after_input = None
                # Вызываем её
                await after_input(
                    message=update.message, 
                    bot_manager=self.bot_manager,
                    user_id=update.message.from_user.id,
                    update=update,
                    context=context)
        self.handle_message = handle_message
    async def get_message_and_run_method(self, user_id: int, function: Callable):
        user_data = self.bot_manager.user_data_manager.get(user_id)
        user_data.after_input = function
    def get_message_handler(self):
        from telegram.ext import MessageHandler
        return MessageHandler(None, self.handle_message)