from .message import Message

class EvaluatedScreen:
    def __init__(self, *menus: Message):
        self.menus: list[Message] = []
        self.extend(*menus)
    
    def extend(self, *menus: Message):
        self.menus.extend(menus)
    
    def clone(self) -> "EvaluatedScreen":
        return EvaluatedScreen(*[menu.clone() for menu in self.menus])
    
    def __repr__(self):
        return f"EvaluatedScreen({",".join([str(menu) for menu in self.menus])})"
    