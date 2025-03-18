from abc import ABC, abstractmethod
from typing import Callable, Iterable, TYPE_CHECKING
from .message import Message

class Screen(ABC):
    def __init__(self, name: str = None):
        self.name = name
        self.messages: list[Message] = []
    
    def append(self, message: Message):
        if not isinstance(message, Message):
            raise ValueError(f"{message=} is not Message")
        self.messages.append(message)
    
    def extend(self, messages: list[Message]):
        for message in messages:
            if not isinstance(message, Message):
                raise ValueError(f"{message=} is not Message")
        self.messages.extend(messages)
    
    @abstractmethod
    def evaluate(self): ...

class StaticScreen(Screen):
    def __init__(self, name: str, *messages: Message):
        super().__init__(name = name)
        self.extend(messages)
    
    def evaluate(self): ...

class DynamicScreen(Screen):
    def __init__(self, name: str, 
            function: Callable[[int], Iterable[Message]]):
        super().__init__(name)
        self.function = function
    def evaluate(self, **kwargs):
        self.messages = self.function(**kwargs)
        if not isinstance(self.menus, Iterable):
            raise ValueError(
f"Dynamic Screen function output = {self.menus} is not Iterable")
        for message in self.messages:
            if not isinstance(message, Message):
                raise ValueError(
f"Dynamic Screen function output contains {message} of wrong type, expected Message")