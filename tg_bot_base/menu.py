from typing import Any, Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from .callback_data import CallbackData
from .evaluated_menu import EvaluatedMenuDefault, EvaluatedMenuPhoto
from .button_rows import ButtonRows



class Menu:
    def __init__(self, name: str, text: str | Callable | None, 
            button_rows: ButtonRows | Callable | None = None, photo: Callable | None = None):
        self.name: str = name
        self.text: str | Callable | None = text
        self.buttons: ButtonRows | Callable | None = button_rows
        self.photo = photo
        from .button_manager import ButtonManager
        self.button_manager: ButtonManager = None
    def handle_callback_data(self, button_to_dict: dict[str, object], user_id: int):
        __callback_data = []
        buttons: InlineKeyboardMarkup = button_to_dict.get("reply_markup")
        for line in buttons:
            for button in line:
                __callback_data.append(button[1])
                button[1] = len(__callback_data) - 1
        self.button_manager.bot_manager.user_local_data.set(user_id, "__callback_data", __callback_data)
    def clone(self):
        buttons_clone = []
        if isinstance(self.buttons, Callable):
            buttons_clone = self.buttons
        else:
            buttons_clone = self.buttons.clone()
        clone = Menu(self.name,self.text,
            buttons_clone
            ,photo=self.photo)
        clone.button_manager = self.button_manager
        return clone
    def get_text(self, **kwargs):
        if callable(self.text):
            return self.text(**kwargs)
        return self.text
    def get_buttons(self, **kwargs):
        if callable(self.buttons):
            return self.buttons(**kwargs)
        return self.buttons
    def get_photo(self, **kwargs) -> list[str]:
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
    def to_dict(self, **kwargs) -> dict:
        result = {}
        result["text"] = self.get_text(**kwargs)
        result["reply_markup"] = Menu.buttons_to_inline_keyboard(self.get_buttons(**kwargs),**kwargs)
        photo = self.get_photo(**kwargs)
        if photo is not None:
            photo = list(map(lambda photo: InputMediaPhoto(media=photo),photo))
            result["photo"] = photo
        return result
    def to_evaluated_menu(self, **kwargs) -> EvaluatedMenuDefault | EvaluatedMenuPhoto:
        if self.photo is not None:
            return EvaluatedMenuPhoto(photo = self.get_photo(**kwargs))
        reply_markup = Menu.buttons_to_inline_keyboard(self.get_buttons(**kwargs),**kwargs)
        return EvaluatedMenuDefault(self.get_text(**kwargs), reply_markup)
            
