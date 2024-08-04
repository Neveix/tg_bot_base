from .button import Button

class ButtonManager:
    __button_dict__ : dict[str, Button]
    def __init__(self, bot):
        self.bot = bot
        self.__button_dict__ = {}
    def add(self, button: Button):
        button.button_manager = self
        self.__button_dict__[button.name] = button
    def get(self, name: str) -> Button:
        return self.__button_dict__.get(name)
