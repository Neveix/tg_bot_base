from .menu import Menu
from .evaluated_screen import EvaluatedScreen

class Screen:
    def __init__(self, name: str, *menus: list[Menu]):
        self.name = name
        self.menus: list[Menu] = []
        self.extend(menus)
    def extend(self, *menus: list[Menu]):
        self.menus.extend(menus)
    def to_evaluated_screen(self, **kwargs) -> EvaluatedScreen:
        return EvaluatedScreen(
            [menu.to_evaluated_menu(**kwargs) for menu in self.menus]
        )
