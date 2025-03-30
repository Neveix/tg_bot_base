from typing import Any


class InputSession:
    def __init__(self, manual_delete: bool = False):
        self.messages = []
        self.manual_delete = manual_delete
        self.directory_level: int = None
    
    def append(self, message: Any):
        self.messages.append(message)