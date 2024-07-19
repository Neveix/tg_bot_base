from typing import Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class Button:
    def __init__(self, name: str, text: str | Callable, buttons: list[list[list[str, str]]] | Callable):
        self.name = name
        self.text = text
        self.buttons = buttons
        self.button_manager = None
    def to_dict(self, **kwargs) -> dict:
        result = {}
        if callable(self.text):
            result["text"] = self.text(**kwargs)
        else:
            result["text"] = self.text
        if callable(self.buttons):
            result["reply_markup"] = self.buttons(**kwargs)
        else:
            result["reply_markup"] = self.buttons
        reply_markup = []
        for y, old_line in enumerate(result["reply_markup"]):
            line = []
            for x, old_button in enumerate(line):
                line.append(InlineKeyboardButton(text = old_button[0], callback_data = old_button[1]))
            reply_markup.append(line)
        result["reply_markup"] = InlineKeyboardMarkup(reply_markup)
        return result