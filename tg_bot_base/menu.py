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
    def to_dict(self, **kwargs) -> dict[str, Any]:
        return self.to_evaluated_menu(**kwargs).to_dict()
    def to_evaluated_menu(self, **kwargs) -> EvaluatedMenuDefault | EvaluatedMenuPhoto:
        if self.photo:
            return EvaluatedMenuPhoto(photo = self.get_photo(**kwargs))
        reply_markup = self.get_buttons(**kwargs).buttons_to_inline_keyboard(**kwargs)
        return EvaluatedMenuDefault(self.get_text(**kwargs), reply_markup)
            
