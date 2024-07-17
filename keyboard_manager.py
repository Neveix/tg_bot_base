from keyboard import Keyboard

class KeyboardManager:
    __keyboard_dict__ : dict[str, Keyboard]
    def __init__(self, bot):
        self.bot = bot
        self.__keyboard_dict__ = {}
    def add(self, keyboard: Keyboard):
        keyboard.keyboard_manager = self
        self.__keyboard_dict__[keyboard.name] = keyboard
    def get(self, name: str) -> Keyboard:
        return self.__keyboard_dict__.get(name)
