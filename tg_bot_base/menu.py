from typing import Any, Callable
from telegram import InputMediaPhoto
from .evaluated_menu import EvaluatedMenuDefault, EvaluatedMenuPhoto
from .button_rows import ButtonRows
from .bot_manager import BotManager



class Menu:
    def __init__(self, 
            text: str | Callable[[BotManager, int], str] | None = None, 
            button_rows: ButtonRows | Callable[[BotManager, int], ButtonRows] | None = None, 
            photo: InputMediaPhoto | Callable[[BotManager, int], InputMediaPhoto] | None = None,
            parse_mode: str | None = None
        ):
        self.text: str | Callable | None = text
        self.buttons:    ButtonRows | Callable | None = button_rows
        self.photo: InputMediaPhoto | Callable | None = photo
        self.parse_mode = parse_mode
        self.bot_manager: BotManager = None
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
        return EvaluatedMenuDefault(self.get_text(**kwargs), self.get_buttons(**kwargs), parse_mode = self.parse_mode)
            
