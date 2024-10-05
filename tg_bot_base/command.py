from telegram.ext import CommandHandler

from typing import Callable

class Command:
    def __init__(self, name: str, action: Callable):
        self.name = name
        self.action = action
        try:
            not self.command_manager
        except AttributeError:
            self.command_manager = None

    def to_command_handler(self) -> CommandHandler:
        return CommandHandler(self.name, self.action)