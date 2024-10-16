from typing import Any, Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from .callback_data import CallbackData
from .evaluated_menu import EvaluatedMenuDefault, EvaluatedMenuPhoto
from .button_rows import ButtonRows
from .bot_manager import BotManager

class Menu:
    def __init__(self, text: str | Callable | None, 
            button_rows: ButtonRows | Callable | None = None, photo: InputMediaPhoto | Callable | None = None):
        self.text: str | Callable | None = text
        self.buttons:    ButtonRows | Callable | None = button_rows
        self.photo: InputMediaPhoto | Callable | None = photo
        self.bot_manager: BotManager = None
    def handle_callback_data(self, button_to_dict: dict[str, object], user_id: int):
        __callback_data = []
        buttons: InlineKeyboardMarkup = button_to_dict.get("reply_markup")
        for line in buttons:
            for button in line:
                __callback_data.append(button[1])
                button[1] = len(__callback_data) - 1
        self.bot_manager.user_local_data.set(user_id, "__callback_data", __callback_data)
    def clone(self) -> "Menu":
        buttons_clone = []
        if isinstance(self.buttons, Callable):
            buttons_clone = self.buttons
        else:
            buttons_clone = self.buttons.clone()
        clone = Menu(self.text,
            buttons_clone
            ,photo=self.photo)
        clone.bot_manager = self.bot_manager
        return clone
    def get_text(self, **kwargs) -> str:
        if callable(self.text):
            return self.text(**kwargs)
        return self.text
    def get_buttons(self, **kwargs) -> ButtonRows:
        if isinstance(self.buttons, Callable):
            return self.buttons(**kwargs)
        return self.buttons
    def get_photo(self, **kwargs) -> InputMediaPhoto:
        if callable(self.photo):
            return self.photo(**kwargs)
        return self.photo
    @staticmethod
    def buttons_to_inline_keyboard(buttons: list[list[str, CallbackData]], 
            set_callback_data: bool=True, **kwargs) -> InlineKeyboardMarkup:
        reply_markup = []
        __callback_data = []
        for old_line in buttons:
            line = []
            for old_button in old_line:
                old_button_text = None
                old_button_callback_data = None
                if callable(old_button):
                    old_button_text, old_button_callback_data = old_button(**kwargs)
                else:
                    old_button_text = old_button[0]
                    old_button_callback_data = old_button[1]
                __callback_data.append(old_button_callback_data)
                line.append(InlineKeyboardButton(text = old_button_text, callback_data = len(__callback_data)-1))
            reply_markup.append(line)
        if set_callback_data:
            kwargs.get("bot_manager").user_local_data.set(kwargs.get("user_id"), "__callback_data", __callback_data)
        return InlineKeyboardMarkup(reply_markup)
    def to_dict(self, **kwargs) -> dict[str, Any]:
        return self.to_evaluated_menu(**kwargs).to_dict()
    def to_evaluated_menu(self, **kwargs) -> EvaluatedMenuDefault | EvaluatedMenuPhoto:
        if self.photo:
            return EvaluatedMenuPhoto(photo = self.get_photo(**kwargs))
        reply_markup = Menu.buttons_to_inline_keyboard(self.get_buttons(**kwargs),**kwargs)
        return EvaluatedMenuDefault(self.get_text(**kwargs), reply_markup)
            
