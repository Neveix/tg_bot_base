from typing import Any
from ..input_session import InputSession as BaseInputSession
from telegram import Message as TgMessage


class InputSession(BaseInputSession):
    def __init__(self, manual_delete: bool = False):
        super().__init__(manual_delete)
        self.messages: list[TgMessage] = []
    
    def append(self, message: TgMessage):
        self.messages.append(message)