from typing import Callable
from telegram import Update
from telegram.ext import CallbackContext

class MessageManager:
    def __init__(self, bot_manager):
        from .bot_manager import BotManager
        self.bot_manager: BotManager = bot_manager
    async def get_message_and_run_method(self, update: Update, context: CallbackContext, edit_text: str, function: Callable, **kwargs):
        self.bot_manager.user_local_data.set(update.message.from_user.id, "__callback_data", None)
        await update.callback_query.edit_message_text(edit_text)
        self.bot_manager.user_local_data.set(
            update.message.from_user.id,
            "__after_input",
            [function,kwargs])