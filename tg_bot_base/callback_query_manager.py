from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import CallbackQuery, Update
from .bot_manager import BotManager
from .menu import Menu
from .callback_data import CallbackData
from .screen import Screen

class UnknownButtonExeption(BaseException):
    pass

class CallbackDataWithNoFunction(BaseException):
    pass

class CallbackQueryManager:
    """
Класс обеспечивает работу обработчика колбэков нажатия на кнопки.
"""
    def __init__(self, bot_manager: BotManager):
        self.bot_manager: BotManager = bot_manager
        self.screen_dict = {}
        async def callback_query_handler(update: Update, context: CallbackContext):
            query = update.callback_query
            user_id: int = query.from_user.id
            await query.answer()
            __callback_data = self.bot_manager.user_local_data.get(user_id, "__callback_data")
            
            if not __callback_data:
                return
            if len(__callback_data) <= int(query.data):
                return
            data: CallbackData = __callback_data[int(query.data)]
            if data.action == "menu":
                await bot_manager.button_manager.simulate_switch_to_menu(*data.args, query=query)
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
        self.callback_query_handler = callback_query_handler
    async def simulate_switch_to_menu(self, menu_name: str, query: CallbackQuery):
        user_id = query.from_user.id
        try:
            menu = self.bot_manager.button_manager.get_clone(menu_name)
        except UnknownButtonExeption:
            return
        __directory_stack = self.bot_manager.user_local_data.get(user_id,"__directory_stack", [])
        if __directory_stack[-1] != menu_name:
            __directory_stack.append(menu_name)
        evaluated_menu = menu.to_evaluated_menu(bot_manager=self.bot_manager, user_id=user_id)
        await self.bot_manager.screen_manager.set_screen(user_id, new_screen=[evaluated_menu])
    async def simulate_step_back(self, query: CallbackQuery):
        user_id = query.from_user.id
        directory_stack = self.bot_manager.user_local_data.get(user_id, "__directory_stack")
        if len(directory_stack) == 1:
            return
        directory_stack.remove(directory_stack[-1])
        menu = self.bot_manager.button_manager.get_clone(directory_stack[-1])
        evaluated_menu = menu.to_evaluated_menu(bot_manager=self.bot_manager, user_id=user_id)
        await self.bot_manager.screen_manager.set_screen(user_id, new_screen=[evaluated_menu])
    async def simulate_show_alert(self, query: CallbackQuery, text: str):
        await query.answer(text=text, show_alert=True)
    def append_screen(self, screen: Screen):
        if not isinstance(screen, Screen):
            raise ValueError(f"{screen=} wrong type")
        for menu in screen.menus:
            menu.button_manager = self
        self.screen_dict[screen.name] = screen
    def extend_screen(self, *screens: list[Screen]):
        for screen in screens:
            self.append_screen(screen)
    def get(self, name: str) -> Menu:
        result = self.screen_dict.get(name)
        if result is None:
            raise KeyError(f"Unknown Screen name {name}")
        return result
    def get_screen_clone(self, name: str) -> Menu:
        return self.get(name).clone()
    def get_callback_query_handler(self) -> CallbackQueryHandler:
        return CallbackQueryHandler(self.callback_query_handler)
