from abc import ABC, abstractmethod
from typing import Any, Sequence

from tg_bot_screen.core.models.button_rows import ButtonRows
from tg_bot_screen.core.models.callback_data_mapping import CallbackDataMapping
from tg_bot_screen.core.models.media_data import (
    Audio,
    Document,
    Photo,
    Video,
    VideoNote,
    Voice,
)
from tg_bot_screen.core.models.message import SentMessage, UnSentMessage
from .models.user_state import UserState
from .models.screen import UnSentScreen, SentScreen
from .models.proto_screen import ProtoScreen


class UserStateStore(ABC):
    @abstractmethod
    def get(self, user_id: int) -> UserState: ...

    @abstractmethod
    def reset(self, user_id: int) -> None: ...

    @abstractmethod
    def set(self, user_id: int, user_data: UserState) -> None: ...


class ScreenService(ABC):
    @abstractmethod
    async def clear(self, user_id: int, delete_messages: bool = True): ...

    @abstractmethod
    async def set_by_screen(self, user_id: int, screen: UnSentScreen): ...

    @abstractmethod
    async def set(
        self,
        user_id: int,
        screen_name: str,
        stack: bool = True,
        raise_on_error: bool = True,
        params: dict[Any, Any] | None = None,
    ) -> None: ...

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
    async def send_message(
        self,
        chat_id: int,
        text: str,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_audio(
        self,
        chat_id: int,
        audio: Audio,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_photo(
        self,
        chat_id: int,
        photo: Photo,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_video(
        self,
        chat_id: int,
        video: Video,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_document(
        self,
        chat_id: int,
        document: Document,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_voice(
        self,
        chat_id: int,
        voice: Voice,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_video_note(
        self,
        chat_id: int,
        video_note: VideoNote,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def delete_message(self, chat_id: int, message_id: int) -> bool:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def edit_message_media(
        self,
        chat_id: int,
        message_id: int,
        media: Photo | Video | Audio | Document,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def edit_message_caption(
        self,
        chat_id: int,
        message_id: int,
        caption: str | None,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass

    @abstractmethod
    async def send_media_group(
        self,
        chat_id: int,
        media: Sequence[Photo | Video | Audio | Document],
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
    ) -> list[int]:
        """
        :raises MessageNotModified:
        :raises BadRequest: when telegram api error
        :raises TgBotScreenException: In any other case
        """
        pass


class ButtonRowsToReplyMarkupConverter(ABC):
    @abstractmethod
    def convert(
        self,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> Any: ...


class MessageSender(ABC):
    @abstractmethod
    async def send(
        self,
        message: UnSentMessage,
        user_id: int,
        mapping: CallbackDataMapping,
    ) -> SentMessage:
        """
        :raises BadRequest:
        :raises TgBotScreenException:
        """
        ...


class MessageEditor(ABC):
    @abstractmethod
    async def edit(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
        mapping: CallbackDataMapping,
    ) -> SentMessage:
        """
        :raises MessageNotModified:
        :raises CannotTransformMessage:
        :raises BadRequest:
        :raises TgBotScreenException:
        """
        ...

    @abstractmethod
    def check_message_can_be_replaced(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
    ) -> bool: ...


class MessageDeleter(ABC):
    @abstractmethod
    async def delete(
        self,
        message: SentMessage,
    ) -> bool:
        """
        :raises BadRequest:
        :raises TgBotScreenException:
        """
        ...
