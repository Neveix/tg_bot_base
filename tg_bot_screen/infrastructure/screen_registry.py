from ..core.models.screen import ProtoScreen
from ..core.interfaces import ScreenRegistry


class ScreenRegistryImpl(ScreenRegistry):
    def __init__(self):
        self.screen_dict: dict[str, ProtoScreen] = {}

    def register(self, screen: ProtoScreen):
        if self.screen_dict.get(screen.name) is not None:
            raise KeyError(
                f"Попытка повторно создать экран с названием {screen.name!r}"
            )
        self.screen_dict[screen.name] = screen

    def get(self, name: str) -> ProtoScreen | None:
        return self.screen_dict.get(name)
