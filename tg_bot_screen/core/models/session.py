from dataclasses import dataclass
from typing import Any

@dataclass(kw_only=True)
class SessionDeleteContext:
    directory_level: int = -1
    last_directory: str = ""

@dataclass
class Session:
    id: str
    delete_if_level_decreased: bool = True
    delete_if_last_dir_changed: bool = False
    
    def __repr__(self):
        return f"{type(self).__name__}(id={self.id!r})"



class InputSession(Session):
    messages: list[Any] = []
    add_new_messages: bool = True
    may_pop_last_input: bool = True
    
    def append(self, message: Any):
        self.messages.append(message)