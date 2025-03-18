from abc import ABC, abstractmethod
from typing import Callable, Iterable

from tg_bot_base.callback_data import CallbackData

from .evaluated_screen import EvaluatedScreen
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
    def evaluate(self) -> tuple[EvaluatedScreen, dict[str, CallbackData]]: ...

class StaticScreen(Screen):
    def __init__(self, name: str, *messages: Message):
        super().__init__(name = name)
        self.extend(messages)
    
    def evaluate(self):
        print(f"Screen {self.name} evaluate called")
        items = []
        messages = []
        for message in self.messages:
            new_message = message.clone()
            messages.append(new_message)
            items.extend(new_message.prepare().items())  
        return EvaluatedScreen(*messages), dict(items)

class DynamicScreen(Screen):
    def __init__(self, name: str, 
            function: Callable[[int], Iterable[Message]]):
        super().__init__(name)
        self.function = function
    
    def evaluate(self, user_id: int):
        messages = self.function(user_id)
        items = []
        for message in messages:
            items.extend(message.prepare().items())  
        return EvaluatedScreen(*messages), dict(items)
        