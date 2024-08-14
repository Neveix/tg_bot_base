from .button import Button
from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from .bot_manager import BotManager

class ButtonManager:
    __button_dict__ : dict[str, Button]
    def __init__(self, bot_manager: BotManager):
        self.bot: BotManager = bot_manager
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
    async def update_button_callback_data(self, user_id, func, *args, **kwargs):
        self.bot_manager.user
        reply_markup: InlineKeyboardMarkup = kwargs.get("reply_markup")
        if reply_markup != None:
            for line in reply_markup.inline_keyboard:
                for button in line:
                    #button.
                    pass
        
    def get_callback_query_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(ButtonManager.__handler_callback__)
