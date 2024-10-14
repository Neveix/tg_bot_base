
from .bot_manager import BotManager
from .evaluated_menu import EvaluatedMenu
class ScreenManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
    def get_screen(self, user_id: int) -> list[EvaluatedMenu] | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        screen = self.bot_manager.user_local_data.get(user_id, "__screen")
        if screen is None:
            return None
        return [evaluated_menu.clone() for evaluated_menu in screen]
    def clear_screen(self, user_id: int):
        self.bot_manager.user_local_data.set(user_id, "__screen", None)
    def set_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        old_screen = self.get_screen(user_id)
        if old_screen is None or len(new_screen) > len(old_screen):
            self._pure_set_screen(user_id, new_screen)
            self.send_screen(user_id, new_screen)
        else:
            any(map(lambda menu: menu, new_screen))
    def send_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        for menu in new_screen:
            menu.send(self.bot_manager.bot, chat_id = user_id)
    def _pure_set_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        self.bot_manager.user_local_data.set(user_id, "__screen", new_screen)