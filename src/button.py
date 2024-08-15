from typing import Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class Button:
    def __init__(self, name: str, text: str | Callable, buttons: list[list[list[str, str]]] | Callable = None):
        from .button_manager import ButtonManager
        self.name = name
        self.text = text
        self.buttons = buttons
        self.button_manager: ButtonManager = None
    def convert_callback_data(self, user_id: int) -> None:
        __callback_data = []
        for line in self.buttons:
            for button in self.buttons:
                __callback_data.append(button[1])
                button[1] = len(__callback_data) - 1
        self.button_manager.bot.user_local_data.set(user_id, "__callback_data", __callback_data)
    def clone(self):
        return Button(self.name,self.text,self.buttons,self.button_manager)
    def to_dict(self, **kwargs) -> dict:
        result = {}
        if callable(self.text):
            result["text"] = self.text(**kwargs)
        else:
            result["text"] = self.text
        if callable(self.buttons):
            result["reply_markup"] = self.buttons(**kwargs)
        elif self.buttons != None:
            result["reply_markup"] = self.buttons
        if result.get("reply_markup") and len(result["reply_markup"]) > 0:
            reply_markup = []
            for y, old_line in enumerate(result["reply_markup"]):
                line = []
                for x, old_button in enumerate(old_line):
                    line.append(InlineKeyboardButton(text = old_button[0], callback_data = old_button[1]))
                reply_markup.append(line)
            result["reply_markup"] = InlineKeyboardMarkup(reply_markup)
        return result