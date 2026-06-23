from abc import ABC, abstractmethod
from typing import Any, Self

from tg_bot_screen.core.models.input_callback_use_params import InputCallbackUseParams
from .models.user_state import UserState
from .models.callback_data_use_params import CallbackDataUseParams
from .models.screen import ProtoScreen, UnSentScreen, SentScreen


class CallbackData(ABC):
    @abstractmethod
    def clone(self) -> Self: ...

    @abstractmethod
    async def use(self, *, params: CallbackDataUseParams, **kwargs): ...


class CallbackDataMapping(ABC):
    @abstractmethod
    def add(self, callback: CallbackData, uuid: str) -> None: ...

    @abstractmethod
    def get_by_callback(self, callback: CallbackData) -> str: ...

    @abstractmethod
    def get_by_uuid(self, uuid: str) -> CallbackData | None: ...


class UserStateStore(ABC):
    @abstractmethod
    def get(self, user_id: int) -> UserState: ...

    @abstractmethod
    def reset(self, user_id: int) -> None: ...

    @abstractmethod
    def set(self, user_id: int, user_data: UserState) -> None: ...


class InputCallback(ABC):
    @abstractmethod
    async def use(
        self,
        *,
        params: InputCallbackUseParams,
    ) -> None: ...


class DirectoryStack(ABC):
    @abstractmethod
    def get_all(self) -> tuple[str, ...]: ...

    @abstractmethod
    def last(self) -> str | None: ...

    @abstractmethod
    def append(self, directory: str) -> None: ...

    @abstractmethod
    def pop(self) -> None: ...

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def __len__(self) -> int: ...


class ScreenService(ABC):
    @abstractmethod
    async def clear(self, user_id: int, delete_messages: bool = True): ...

    @abstractmethod
    async def set(self, user_id: int, screen: UnSentScreen): ...

    @abstractmethod
    async def set_by_name(
        self, user_id: int, screen_name: str, stack: bool = True, **kwargs
    ): ...

    @abstractmethod
    async def update(self, user_id: int): ...

    @abstractmethod
    async def step_back(self, user_id: int, times: int = 1) -> None: ...

    @abstractmethod
    async def buffer(self, user_id: int): ...

    @abstractmethod
    async def unbuffer(self, user_id: int): ...

    @abstractmethod
    def get(self, user_id: int) -> SentScreen | None: ...


class ScreenRegistry(ABC):
    @abstractmethod
    def register(self, screen: ProtoScreen) -> None: ...

    @abstractmethod
    def get(self, name: str) -> ProtoScreen | None: ...


class BotAdapter(ABC):
    @abstractmethod
    async def delete_message(self, chat_id: int, message_id: int): ...

    @abstractmethod
    async def edit_text(
        self, chat_id: int, message_id: int, text: str, reply_markup
    ): ...

    @abstractmethod
    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup,
    ) -> Any: ...

    @abstractmethod
    async def send_photo(
        self,
        chat_id: int,
        photo,
        caption: str,
        reply_markup,
    ) -> Any: ...
