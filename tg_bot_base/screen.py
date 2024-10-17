from typing import Tuple
from .menu import Menu
from .evaluated_screen import EvaluatedScreen

class Screen:
    def __init__(self, name: str, *menus: Menu):
        if not isinstance(menus, Tuple):
            raise ValueError(f"{menus=} is not Tuple")
        self.name = name
        self.menus: list[Menu] = []
        self.extend(*menus)
    def extend(self, *menus: Menu):
        for menu in menus:
            if not isinstance(menu, Menu):
                raise ValueError(f"{menu=} is not of type {Menu}")
            self.menus.append(menu)
    def to_evaluated_screen(self, **kwargs) -> EvaluatedScreen:
        return EvaluatedScreen(
            *[menu.to_evaluated_menu(**kwargs) for menu in self.menus]
        )
