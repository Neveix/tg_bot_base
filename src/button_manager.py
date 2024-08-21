from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from .bot_manager import BotManager
from .button import Button

class UnknownButtonExeption(BaseException):
    pass

class ButtonManager:
    __button_dict__ : dict[str, Button]
    def __init__(self, bot_manager: BotManager):
        self.bot_manager: BotManager = bot_manager
        self.__button_dict__ = {}
        async def __handler_callback(update: Update, context: CallbackContext):
            query = update.callback_query
            user_id: int = query.from_user.id
            data = self.bot_manager.user_local_data.get(user_id, "__callback_data")[int(query.data)]
            await query.answer()
            if data[0] == "button":
                button = self.get_clone(data[1])
                button.convert_callback_data(user_id)
                self.bot_manager.user_local_data.append(user_id, "__directory_stack", data[1])
                await query.edit_message_text(**button.to_dict())
            elif data[0] == "step_back":
                directory_stack = self.bot_manager.user_local_data.get(user_id, "__directory_stack")
                if len(directory_stack) == 1:
                    return
                directory_stack.remove(directory_stack[-1])
                button = self.get_clone(directory_stack[-1])
                button.convert_callback_data(user_id)
                await query.edit_message_text(**button.to_dict())
                
        self.__handler_callback = __handler_callback
    def add(self, button: Button):
        button.button_manager = self
        self.__button_dict__[button.name] = button
    def add_many(self, *buttons):
        for button in buttons:
            self.add(button)
    def get(self, name: str) -> Button:
        result = self.__button_dict__.get(name)
        if result==None:
            raise UnknownButtonExeption(f"Unknown button name {name}")
        return result
    def get_clone(self, name: str) -> Button:
        return self.get(name).clone()
    def get_callback_query_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.__handler_callback)
