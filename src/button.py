from typing import Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class Button:
    def __init__(self, name: str, text: str | Callable, buttons: list[list[list[str, object] | Callable]] | Callable = None, button_manager = None):
        from .button_manager import ButtonManager
        self.name = name
        self.text = text
        self.buttons = buttons
        self.button_manager: ButtonManager = button_manager
    def convert_callback_data(self, user_id: int) -> None:
        __callback_data = []
        buttons = self.get_buttons()
        for line in buttons:
            for button in line:
                __callback_data.append(button[1])
                button[1] = len(__callback_data) - 1
        self.button_manager.bot_manager.user_local_data.set(user_id, "__callback_data", __callback_data)
    def clone(self):
        buttons_clone = []
        if callable(self.buttons):
            buttons_clone = self.buttons
        else:
            for line in self.buttons:
                newline = []
                buttons_clone.append(newline)
                for button in line:
                    new_button = button
                    if not callable(button):
                        new_button = list(button)
                    newline.append(new_button)
        return Button(self.name,self.text,
            buttons_clone
            ,self.button_manager)
    def get_text(self, **kwargs):
        if callable(self.text):
            return self.text(**kwargs)
        else:
            return self.text
    def get_buttons(self, **kwargs):
        if callable(self.buttons):
            return self.buttons(**kwargs)
        else:
            return self.buttons
    def to_dict(self, **kwargs) -> dict:
        result = {}
        result["text"] = self.get_text(**kwargs)
        result["reply_markup"] = self.get_buttons(**kwargs)
        if result.get("reply_markup") and len(result["reply_markup"]) > 0:
            reply_markup = []
            for old_line in result["reply_markup"]:
                line = []
                for old_button in old_line:
                    old_button_text = old_button[0]
                    old_button_callback_data = old_button[1]
                    if callable(old_button):
                        old_button_text, old_button_callback_data = old_button(**kwargs)
                    line.append(InlineKeyboardButton(text = old_button_text, callback_data = old_button_callback_data))
                reply_markup.append(line)
            result["reply_markup"] = InlineKeyboardMarkup(reply_markup)
        return result