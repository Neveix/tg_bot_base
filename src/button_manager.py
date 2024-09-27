from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import CallbackQuery, InputMedia, InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup
from .bot_manager import BotManager
from .button import Button
from tg_bot_base.src.callback_data import CallbackData

class UnknownButtonExeption(BaseException):
    pass

class CallbackDataWithNoFunction(BaseException):
    pass

class ButtonManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager: BotManager = bot_manager
        self.__button_dict__ = {}
        async def handle_callback(update: Update, context: CallbackContext):
            query = update.callback_query
            user_id: int = query.from_user.id
            await query.answer()
            __callback_data = self.bot_manager.user_local_data.get(user_id, "__callback_data")
            if not __callback_data:
                return
            if len(__callback_data) <= int(query.data):
                return
            data: CallbackData = __callback_data[int(query.data)]
            if data.action == "button":
                await bot_manager.button_manager.simulate_switch_to_button(*data.args, query=query)
            elif data.action == "step_back":
                await bot_manager.button_manager.simulate_step_back(query=query)
            elif data.action == "function":
                function = data.args[0]
                if not callable(function):
                    raise CallbackDataWithNoFunction
                args = data.args[1:]
                await function(bot_manager=self.bot_manager, 
                    button_manager=self, update=update, context=context, user_id=user_id, *args, **data.kwargs)
            elif data.action == "show_alert":
                await bot_manager.button_manager.simulate_show_alert(query=query, text = data.args[0])
        self.handle_callback = handle_callback
    async def simulate_switch_to_button(self, button_name: str, query: CallbackQuery):
        user_id = query.from_user.id
        try:
            button = self.bot_manager.button_manager.get_clone(button_name)
        except UnknownButtonExeption:
            return
        self.bot_manager.user_local_data.append(user_id, "__directory_stack", button_name)
        button_dict = button.to_dict(user_id=user_id,bot_manager=self.bot_manager)
        button_text_and_markup = {}
        button_text_and_markup["text"]= button_dict.get("text")
        button_text_and_markup["reply_markup"]= button_dict.get("reply_markup")
        await query.edit_message_text(**button_text_and_markup)
        photo_ids = button_dict.get("photos")
        if photo_ids != None:
            await query.edit_message_media(media = photo_ids)
    async def simulate_step_back(self, query: CallbackQuery):
        user_id = query.from_user.id
        directory_stack = self.bot_manager.user_local_data.get(user_id, "__directory_stack")
        if len(directory_stack) == 1:
            return
        directory_stack.remove(directory_stack[-1])
        button = self.bot_manager.button_manager.get_clone(directory_stack[-1])
        await query.edit_message_text(**button.to_dict(user_id=user_id,bot_manager=self.bot_manager))
    async def simulate_show_alert(self, query: CallbackQuery, text: str):
        await query.answer(text=text, show_alert=True)
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
        return CallbackQueryHandler(self.handle_callback)
