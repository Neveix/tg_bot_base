from abc import ABC, abstractmethod
from typing import Callable, Iterable
from .callback_data import CallbackData
from .message import Message, SentMessage

class HasCallbackData(ABC):
    @abstractmethod
    def __init__(self): ...
    
    def get_callback_data(self):
        result: list[CallbackData] = []
        for message in self.messages:
            result.extend(message.get_callback_data())
        return result

class ReadyScreen(HasCallbackData):
    def __init__(self, *messages: Message):
        self.messages: list[Message] = []
        self.extend(messages)
    
    def extend(self, messages: list[Message]):
        self.messages.extend(messages)
    
    def clone(self) -> "ReadyScreen":
        return ReadyScreen(*[message.clone() for message in self.messages])

class SentScreen(HasCallbackData):
    def __init__(self, *messages: SentMessage):
        self.messages: list[SentMessage] = []
        self.extend(messages)
    
    def extend(self, messages: list[SentMessage]):
        self.messages.extend(messages)
        
    def clone(self) -> "SentScreen":
        return SentScreen(*[message.clone() for message in self.messages])
    
    @abstractmethod
    async def delete(self): ...
    
    @abstractmethod
    def get_unsent(self): ...

class ProtoScreen(ABC):
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
    def evaluate(self) -> tuple[ReadyScreen, dict[str, CallbackData]]: ...

class StaticScreen(ProtoScreen):
    def __init__(self, name: str, *messages: Message):
        super().__init__(name = name)
        self.extend(messages)
    
    def evaluate(self):
        messages = []
        for message in self.messages:
            new_message = message.clone()
            messages.append(new_message)
        return ReadyScreen(*messages)

class DynamicScreen(ProtoScreen):
    def __init__(self, name: str, 
            function: Callable[[int], Iterable[Message]]):
        super().__init__(name)
        self.function = function
    
    def evaluate(self, user_id: int):
        return ReadyScreen(*self.function(user_id))


