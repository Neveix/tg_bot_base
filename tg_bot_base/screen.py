from .menu import Menu

class Screen:
    def __init__(self, name: str, *menus: list[Menu]):
        self.name = name
        self.menus: list[Menu] = []
        self.extend(menus)
    def extend(self, *menus: list[Menu]):
        self.menus.extend(menus)
