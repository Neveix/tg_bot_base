from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from ..interfaces import BotAdapter, CallbackData, CallbackDataMapping
from .button_rows import ButtonRows


class MessageCategory(StrEnum):
    SIMPLE = "simple"
    MEDIA = "media"
    VIDEO_NOTE = "video_note"


class ParseMode(StrEnum):
    MARKDOWN = "markdown"
    HTML = "html"


@dataclass(kw_only=True)
class HasTextMixin:
    text: str
    parse_mode: ParseMode | None = None


class HasReplyMarkup(ABC):
    @abstractmethod
    def get_reply_markup(self, *args, **kwargs): ...


@dataclass(kw_only=True)
class HasButtonRowsMixin:
    button_rows: ButtonRows | None = None

    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()


class UnSentMessage(HasButtonRowsMixin, HasReplyMarkup):
    def __init__(
        self,
        *,
        category: MessageCategory,
        button_rows: ButtonRows | None = None,
    ):
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        self.category = category

    @abstractmethod
    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> "SentMessage": ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def clone(self) -> Self: ...


class SentMessage(HasButtonRowsMixin):
    def __init__(
        self, category: MessageCategory, button_rows: ButtonRows | None = None
    ):
        super().__init__(button_rows=button_rows)
        self.category = category

    @abstractmethod
    async def delete(
        self,
        bot_adapter: BotAdapter,
    ): ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def clone(self) -> Self: ...

    @abstractmethod
    def get_unsent(self) -> UnSentMessage: ...

    @abstractmethod
    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self: ...


Message = UnSentMessage | SentMessage


class MediaMessage(HasTextMixin, HasButtonRowsMixin):
    def __init__(
        self,
        *,
        text: str,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        self.category: MessageCategory = MessageCategory.MEDIA

    def __new__(cls, *args, **kwargs):
        assert cls is not MediaMessage, (
            f"{cls.__name__} cannot be created directly, only its subclasses"
        )
        return super().__new__(cls)


class SimpleMessage(UnSentMessage, HasTextMixin):
    def __init__(
        self,
        text: str,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        UnSentMessage.__init__(
            self, button_rows=button_rows, category=MessageCategory.SIMPLE
        )
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)


class AudioMessage(MediaMessage, UnSentMessage): ...


class DocumentMessage(MediaMessage, UnSentMessage): ...


class PhotoMessage(MediaMessage, UnSentMessage): ...


class VideoMessage(MediaMessage, UnSentMessage): ...


class VideoNoteMessage(UnSentMessage):
    def __init__(
        self,
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(
            category=MessageCategory.VIDEO_NOTE,
            button_rows=button_rows,
        )


# ----- #


class SentAudioMessage(MediaMessage, SentMessage): ...


class SentDocumentMessage(MediaMessage, SentMessage): ...


class SentSimpleMessage(SentMessage, HasTextMixin):
    def __init__(
        self,
        text: str,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        super().__init__(category=MessageCategory.SIMPLE, button_rows=button_rows)
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)


class SentPhotoMessage(MediaMessage, SentMessage): ...


class SentVideoMessage(MediaMessage, SentMessage): ...


class SentVideoNoteMessage(SentMessage):
    def __init__(
        self,
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(MessageCategory.VIDEO_NOTE, button_rows)
