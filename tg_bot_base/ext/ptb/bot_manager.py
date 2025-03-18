from telegram import Update
from telegram.ext import Application, CallbackQueryHandler
from ...user_data import UserDataManager
from ...bot_manager import BotManager as BaseBotManager
from .user_screen import UserScreen

class BotManager(BaseBotManager):
    def __init__(self, application: Application):
        super().__init__()
        self.bot = application.bot
        self.application = application
    
    def build(self):
        user_data = UserDataManager()
        screen = UserScreen(user_data, self.bot)
        self.user_data = user_data
        self.screen = screen
        return self
    
    def get_callback_query_handler(self):
        async def callback(update: Update, _):
            user_id = update.callback_query.from_user.id
            query_data = update.callback_query.data
            await self._handle_callback_query(user_id, query_data)
            await update.callback_query.answer()
        return CallbackQueryHandler(callback)
            

    def get_message_handler(self):
        pass