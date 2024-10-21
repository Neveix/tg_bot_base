from .evaluated_menu import EvaluatedMenu

class EvaluatedScreen:
    def __init__(self, *menus: EvaluatedMenu):
        self.menus: list[EvaluatedMenu] = []
        self.extend(*menus)
    def extend(self, *menus: EvaluatedMenu):
        self.menus.extend(menus)
    def clone(self) -> "EvaluatedScreen":
        return EvaluatedScreen(*[menu.clone() for menu in self.menus])
    def __repr__(self):
        return f"EvaluatedScreen({",".join([str(menu) for menu in self.menus])})"