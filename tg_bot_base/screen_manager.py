
from .bot_manager import BotManager

class ScreenManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
    def get_screen(self):
        pass
    def set_screen(self, screen):
        pass
    def update_screen(self):
        pass
