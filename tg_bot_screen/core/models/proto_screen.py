from abc import ABC, abstractmethod
from typing import Any, Iterable, Protocol, runtime_checkable

from tg_bot_screen.core.models.message import UnSentMessage
from tg_bot_screen.core.models.screen import UnSentScreen
from tg_bot_screen.core.models.user_state import UserState


class ProtoScreen(ABC):
    def __init__(self, name: str):
        self.name = name
        self.messages: list[UnSentMessage] = []

    def append(self, message: UnSentMessage):
        self.messages.append(message)

    def extend(self, messages: list[UnSentMessage]):
        for message in messages:
            self.append(message)

    @abstractmethod
    async def evaluate(
        self,
        user_id: int,
        us: UserState,
        params: dict[Any, Any] | None,
    ) -> UnSentScreen: ...


class StaticScreen(ProtoScreen):
    def __init__(self, name: str, *messages: UnSentMessage):
        super().__init__(name=name)
        self.extend(list(messages))

    async def evaluate(
        self, user_id: int, us: UserState, params: dict[Any, Any] | None
    ):
        messages = []
        for message in self.messages:
            new_message = message.clone()
            messages.append(new_message)
        return UnSentScreen(*messages)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.messages!r})"


@runtime_checkable
class DynamicScreenEvaluateFunction(Protocol):
    async def __call__(
        self,
        *,
        user_id: int,
        us: UserState,
        params: dict[Any, Any],
    ) -> Iterable[UnSentMessage]: ...


class DynamicScreen(ProtoScreen):
    def __init__(self, name: str, function: DynamicScreenEvaluateFunction):
        super().__init__(name)
        self.function = function

    async def evaluate(
        self, user_id: int, us: UserState, params: dict[Any, Any] | None
    ):
        params = params or dict()
        messages = await self.function(user_id=user_id, us=us, params=params)
        return UnSentScreen(*messages)

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.function!r})"
