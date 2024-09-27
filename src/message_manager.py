from typing import Callable
from telegram import Update
from telegram.ext import CallbackContext

class MessageManager:
    def __init__(self, bot_manager):
        from .bot_manager import BotManager
        self.bot_manager: BotManager = bot_manager
        async def handle_message(update: Update, context: CallbackContext):
            __media_group_id = self.bot_manager.user_local_data.get(
                update.message.from_user.id,
                "__media_group_id")
            if update.message.media_group_id != None:
                if __media_group_id == update.message.media_group_id:
                    return
                self.bot_manager.user_local_data.set(
                    update.message.from_user.id,
                    "__media_group_id",
                    update.message.media_group_id)
            __after_input = self.bot_manager.user_local_data.get(
                update.message.from_user.id,
                "__after_input")
            if callable(__after_input):
                self.bot_manager.user_local_data.set(
                    update.message.from_user.id,
                    "__after_input", None)
                await __after_input(
                    message=update.message, 
                    bot_manager=self.bot_manager,
                    update=update,
                    context=context
                )
        self.handle_message = handle_message
    async def get_message_and_run_method(self, user_id: int, function: Callable):
        self.bot_manager.user_local_data.set(user_id, "__callback_data", None)
        self.bot_manager.user_local_data.set(
            user_id,
            "__after_input",
            function)
    def get_message_handler(self):
        from telegram.ext import MessageHandler
        return MessageHandler(None, self.handle_message)
    async def reply_message_button(self, button_name: str, update: Update):
        button = self.bot_manager.button_manager.get_clone(button_name)
        user_id = update.message.from_user.id
        if self.bot_manager.user_local_data.get(user_id,"__directory_stack",[])[-1] != button.name:
            self.bot_manager.user_local_data.append(user_id, "__directory_stack",button.name)
        await update.message.reply_text(**button.to_dict(user_id=user_id,bot_manager=self.bot_manager))