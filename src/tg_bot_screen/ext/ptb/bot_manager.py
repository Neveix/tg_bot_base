from telegram import Update
from telegram import Message as TgMessage
from telegram.ext import Application, CallbackQueryHandler, MessageHandler
from ...user_data import UserDataManager
from ...bot_manager import BotManager as BaseBotManager
from .user_screen import UserScreen

class BotManager(BaseBotManager):
    def __init__(self, application: Application):
        super().__init__()
        self.bot = application.bot
        self.application = application
    
    def get_callback_query_handler(self):
        async def callback(update: Update, _):
            user_id = update.callback_query.from_user.id
            query_data = update.callback_query.data
            await self._handle_callback_query(user_id, query_data)
            await update.callback_query.answer()
        return CallbackQueryHandler(callback)

    def get_message_handler(self):
        async def callback(update: Update, _):
            user_id = update.message.from_user.id
            await self._handle_message(user_id, update=update
                , message=update.message)
            
        return MessageHandler(None, callback)
    
    async def delete_message(self, message: TgMessage, **kwargs):
        await message.delete()