from typing import Callable
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, PhotoSize, InputMediaPhoto

class Button:
    def __init__(self, name: str, text: str | Callable, buttons: list[list[list[str, object] | Callable]] | Callable = None, photos=None):
        from .button_manager import ButtonManager
        self.name = name
        self.text = text
        self.buttons = buttons
        self.photos = photos
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
        clone = Button(self.name,self.text,
            buttons_clone
            ,photos=self.photos)
        clone.button_manager = self.button_manager
        return clone
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
    def get_photos(self, **kwargs) -> list[str]:
        if callable(self.photos):
            return self.photos(**kwargs)
        else:
            return self.photos
    def to_dict(self, **kwargs) -> dict:
        user_id = kwargs.get("user_id")
        result = {}
        result["text"] = self.get_text(**kwargs)
        result["reply_markup"] = self.get_buttons(**kwargs)
        if result.get("reply_markup") and len(result["reply_markup"]) > 0:
            reply_markup = []
            __callback_data = []
            for old_line in result["reply_markup"]:
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
            result["reply_markup"] = InlineKeyboardMarkup(reply_markup)
            self.button_manager.bot_manager.user_local_data.set(user_id, "__callback_data", __callback_data)
        photos = self.get_photos(**kwargs)
        if photos != None:
            photos = list(map(lambda photo: InputMediaPhoto(media=photo),photos))
            result["photos"] = photos
        return result