from telegram.ext import Application
from ... import BotManager as BaseBotManager


class BotManager(BaseBotManager):
    def __init__(self, application: Application):
        super().__init__()
        self.bot = application.bot
        self.application = application
