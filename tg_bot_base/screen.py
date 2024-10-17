from typing import Callable, Iterable
from .bot_manager import BotManager
from .menu import Menu
from .evaluated_screen import EvaluatedScreen

class Screen:
    """Базовый класс для Статического и Динамического экранов. 
Его использование не предполагается"""
    def __init__(self, name: str | None = None):
        self.name = name
        self.menus: list[Menu] = []
    def append(self, menu: Menu):
        if not isinstance(menu, Menu):
            raise ValueError(f"{menu=} is not of type {Menu}")
        self.menus.append(menu)
    def extend(self, *menus: Menu):
        for menu in menus:
            self.append(menu)
    def to_evaluated_screen(self, **kwargs) -> EvaluatedScreen:
        return EvaluatedScreen(
            *[menu.to_evaluated_menu(**kwargs) for menu in self.menus]
        )

class StaticScreen(Screen):
    """Статический экран с фиксированным количеством Меню"""
    def __init__(self, *menus: Menu, name: str | None = None):
        super().__init__(name = name)
        self.extend(*menus)
class DynamicScreen(Screen):
    def __init__(self, 
            function: Callable[[BotManager, int], Iterable[Menu]], 
            name: str | None = None):
        super().__init__(name)
        self.function = function
    def to_evaluated_screen(self, **kwargs):
        self.menus = self.function(**kwargs)
        if not isinstance(self.menus, Iterable):
            raise ValueError(f"Dynamic Screen function output = {self.menus} is not Iterable")
        for menu in self.menus:
            if not isinstance(menu, Menu):
                raise ValueError(f"Dynamic Screen function output contains {menu} of wrong type, expected Menu")
        return super().to_evaluated_screen(**kwargs)