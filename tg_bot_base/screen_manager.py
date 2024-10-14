
from .bot_manager import BotManager
from .evaluated_menu import EvaluatedMenu, EvaluatedMenuDefault, EvaluatedMenuPhoto

class ScreenManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
        self.screen = None
    def get_screen(self) -> list[EvaluatedMenu] | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        return [evaluated_menu.clone() for evaluated_menu in self.screen]
    def set_screen(self, screen: list[EvaluatedMenu]):
        self.screen = screen
