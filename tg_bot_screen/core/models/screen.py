from inspect import iscoroutinefunction
from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Self, Sequence

from .error_info import check_bad_value
from .callback_data import CallbackData
from .message import HasButtonRows, UnSentMessage, SentMessage

class HasCallbackData(ABC):
   
    @abstractmethod
    def get_callback_data(self) -> list[CallbackData]:
        ...
    
    
class HasCallbackDataMixin(HasCallbackData):
    @abstractmethod
    def get_messages_for_callback_data(self) -> Sequence[HasButtonRows]:
        ...
    
    def get_callback_data(self) -> list[CallbackData]:
        result: list[CallbackData] = []
        for message in self.get_messages_for_callback_data():
            result.extend(message.get_callback_data())
        return result


class UnSentScreen(HasCallbackDataMixin):
    def __init__(self, *messages: UnSentMessage):
        self.messages: list[UnSentMessage] = []
        self.extend(list(messages))
    
    def get_messages_for_callback_data(self):
        return self.messages
    
    def extend(self, messages: list[UnSentMessage]):
        for message in messages:
            self.append(message)
        
    def append(self, message: UnSentMessage):
        check_bad_value(message, UnSentMessage, self, "message")
        self.messages.append(message)
    
    def __repr__(self):
        return f"{type(self).__name__}({self.messages!r})"
    
    def clone(self) -> "UnSentScreen":
        return UnSentScreen(*[message.clone() for message in self.messages])


class SentScreen(HasCallbackData):
    def __init__(self, *messages: SentMessage):
        self.messages: list[SentMessage] = []
        self.extend(list(messages))
    
    def extend(self, messages: list[SentMessage]):
        for message in messages:
            self.append(message)
        
    def append(self, message: SentMessage):
        check_bad_value(message, SentMessage, self, "message")
        self.messages.append(message)
        
    def clone(self) -> Self:
        return self.__class__(*[message.clone() 
                                for message in self.messages])
    
    def __repr__(self):
        return f"{type(self).__name__}({self.messages!r})"
    
    @abstractmethod
    async def delete(self, *args, **kwargs): ...
    
    @abstractmethod
    def get_unsent(self) -> UnSentScreen: ...


class ProtoScreen(ABC):
    def __init__(self, name: str):
        self.name = name
        self.messages: list[UnSentMessage] = []
    
    def append(self, message: UnSentMessage):
        check_bad_value(message, UnSentMessage, self, "message")
        self.messages.append(message)
    
    def extend(self, messages: list[UnSentMessage]):
        for message in messages:
            self.append(message)
    
    @abstractmethod
    async def evaluate(self, user_id: int, *args, 
                       **kwargs) -> UnSentScreen: ...


class StaticScreen(ProtoScreen):
    def __init__(self, name: str, *messages: UnSentMessage):
        super().__init__(name = name)
        self.extend(list(messages))
    
    async def evaluate(self, user_id: int, *args, **kwargs):
        messages = []
        for message in self.messages:
            new_message = message.clone()
            messages.append(new_message)
        return UnSentScreen(*messages)
    
    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.messages!r})"



class DynamicScreenEvaluateFunction(Protocol):
    async def __call__(self, *, 
        user_id: int, **kwargs
    ) -> Iterable[UnSentMessage]: 
        ...


class DynamicScreen(ProtoScreen):
    def __init__(self, name: str, 
            function: DynamicScreenEvaluateFunction):
        super().__init__(name)
        if not iscoroutinefunction(function):
            print(f"Экран {name} был создан с не async функцией")
        self.function = function
    
    async def evaluate(self, user_id: int, **kwargs):
        messages = await self.function(user_id=user_id, **kwargs)
        return UnSentScreen(*messages)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.function!r})"

