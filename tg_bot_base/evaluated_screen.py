from .evaluated_menu import EvaluatedMenu

class EvaluatedScreen:
    def __init__(self, *menus: list[EvaluatedMenu]):
        self.menus: list[EvaluatedMenu] = []
        self.extend(*menus)
    def extend(self, *menus: list[EvaluatedMenu]):
        self.menus.extend(menus)
    def clone(self) -> "EvaluatedScreen":
        return EvaluatedScreen(*[menu.clone() for menu in self.menus])