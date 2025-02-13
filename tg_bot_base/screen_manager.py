
from typing import TYPE_CHECKING
from .screen import Screen
if TYPE_CHECKING:
    from .bot_manager import BotManager

class ScreenManager:
    """
Класс для управления сохранёнными экранами
Позволяет их добавлять, получать, получать копии.
"""
    def __init__(self, bot_manager: "BotManager"):
        self.bot_manager = bot_manager
        self.screen_dict = {}
    def append_screen(self, screen: Screen):
        if not isinstance(screen, Screen):
            raise ValueError(f"{screen=} wrong type")
        for menu in screen.menus:
            menu.bot_manager = self.bot_manager
        self.screen_dict[screen.name] = screen
    def extend_screen(self, *screens: list[Screen]):
        for screen in screens:
            self.append_screen(screen)
    def get_screen(self, name: str) -> Screen:
        result = self.screen_dict.get(name)
        if result is None:
            raise KeyError(f"Unknown Screen name {name}")
        return result
    def get_screen_clone(self, name: str) -> Screen:
        return self.get_screen(name).clone()
    
