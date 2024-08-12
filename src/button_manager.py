from .button import Button
from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update

class ButtonManager:
    __button_dict__ : dict[str, Button]
    def __init__(self, bot):
        self.bot = bot
        self.__button_dict__ = {}
    def add(self, button: Button):
        button.button_manager = self
        self.__button_dict__[button.name] = button
    def get(self, name: str) -> Button:
        return self.__button_dict__.get(name)
    async def __handler_callback__(update: Update, context: CallbackContext):
        query = update.callback_query
        userid: int = query.from_user.id
        data: str = query.data
        
    def get_callback_query_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(ButtonManager.__handler_callback__)
