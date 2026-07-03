from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Sequence, runtime_checkable

from ..guards import check_bad_value
from .callback_data import CallbackData
from .message import HasButtonRowsMixin, UnSentMessage, SentMessage


class HasCallbackDataMixin:
    @abstractmethod
    def get_messages_for_callback_data(self) -> Sequence[HasButtonRowsMixin]: ...

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
        return [msg for msg in self.messages if isinstance(msg, HasButtonRowsMixin)]

    def extend(self, messages: list[UnSentMessage]):
        for message in messages:
            self.append(message)

    def append(self, message: UnSentMessage):
        check_bad_value(message, UnSentMessage, self, "message")
        self.messages.append(message)

    def __repr__(self):
        return f"{type(self).__name__}({self.messages!r})"


class SentScreen(HasCallbackDataMixin):
    def __init__(self, *messages: SentMessage):
        self.messages: list[SentMessage] = list(messages)

    def get_messages_for_callback_data(self):
        return [msg for msg in self.messages if isinstance(msg, HasButtonRowsMixin)]

    def extend(self, messages: list[SentMessage]):
        for message in messages:
            self.append(message)

    def append(self, message: SentMessage):
        self.messages.append(message)

    def __repr__(self):
        return f"{type(self).__name__}({self.messages!r})"

    def get_unsent(self) -> UnSentScreen:
        return UnSentScreen(*[message.get_unsent() for message in self.messages])


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
    async def evaluate(self, user_id: int, *args, **kwargs) -> UnSentScreen: ...


class StaticScreen(ProtoScreen):
    def __init__(self, name: str, *messages: UnSentMessage):
        super().__init__(name=name)
        self.extend(list(messages))

    async def evaluate(self, user_id: int, *args, **kwargs):
        messages = []
        for message in self.messages:
            new_message = message.clone()
            messages.append(new_message)
        return UnSentScreen(*messages)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.messages!r})"


@runtime_checkable
class DynamicScreenEvaluateFunction(Protocol):
    async def __call__(self, *, user_id: int, **kwargs) -> Iterable[UnSentMessage]: ...


class DynamicScreen(ProtoScreen):
    def __init__(self, name: str, function: DynamicScreenEvaluateFunction):
        super().__init__(name)
        self.function = function

    async def evaluate(self, user_id: int, **kwargs):
        messages = await self.function(user_id=user_id, **kwargs)
        return UnSentScreen(*messages)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.function!r})"
