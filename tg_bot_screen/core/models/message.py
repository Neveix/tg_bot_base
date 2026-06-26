from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from tg_bot_screen.core.exceptions import CannotTransformMessage
from tg_bot_screen.core.models.media_data import (
    Audio,
    Document,
    Photo,
    Video,
    VideoNote,
)

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


@dataclass(kw_only=True)
class HasButtonRowsMixin:
    button_rows: ButtonRows | None = None

    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()


class UnSentMessage(HasButtonRowsMixin):
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


class SentMessage(HasButtonRowsMixin, ABC):
    def __init__(
        self,
        category: MessageCategory,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(button_rows=button_rows)
        self.category = category
        self.message_id = message_id
        self.user_id = user_id

    async def delete(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
    ):
        result = await bot_adapter.delete_message(
            chat_id=user_id,
            message_id=self.message_id,
        )

        return result

    @abstractmethod
    def get_unsent(self) -> UnSentMessage: ...

    def check_edit_into_message_type(
        self,
        new_message: UnSentMessage,
        edit_into_allowed: list[type[UnSentMessage]],
    ) -> None:
        for msg_type in edit_into_allowed:
            if isinstance(new_message, msg_type):
                break
        else:
            raise CannotTransformMessage(
                f"{type(self)} cannot be transformed into {type(new_message)}"
            )

    @abstractmethod
    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self: ...


Message = UnSentMessage | SentMessage


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

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_message(
            chat_id=user_id,
            text=self.text,
            mapping=mapping,
            parse_mode=self.parse_mode,
            button_rows=self.button_rows,
        )

        return SentSimpleMessage(
            text=self.text,
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


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


class AudioMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        audio: Audio,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.audio = audio
        super().__init__(
            text=text,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_audio(
            chat_id=user_id,
            audio=self.audio,
            text=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentAudioMessage(
            text=self.text,
            audio=self.audio,
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class DocumentMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        document: Document,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.document = document
        super().__init__(
            text=text,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_document(
            chat_id=user_id,
            document=self.document,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentDocumentMessage(
            text=self.text,
            document=self.document,
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class PhotoMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        photo: Photo,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.photo = photo
        super().__init__(
            text=text,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_photo(
            chat_id=user_id,
            photo=self.photo,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentPhotoMessage(
            text=self.text,
            photo=self.photo,
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class VideoMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        video: Video,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.video = video
        super().__init__(
            text=text,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_video(
            chat_id=user_id,
            video=self.video,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentVideoMessage(
            text=self.text,
            video=self.video,
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class VideoNoteMessage(UnSentMessage):
    def __init__(
        self,
        video_note: VideoNote,
        button_rows: ButtonRows | None = None,
    ):
        self.video_note = video_note
        super().__init__(
            category=MessageCategory.VIDEO_NOTE,
            button_rows=button_rows,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_video_note(
            chat_id=user_id,
            video_note=self.video_note,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentVideoNoteMessage(
            message_id=message_id,
            user_id=user_id,
            button_rows=self.button_rows,
        )


# ----- #


class SentSimpleMessage(SentMessage, HasTextMixin):
    def __init__(
        self,
        text: str,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        super().__init__(
            category=MessageCategory.SIMPLE,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
        )
        HasTextMixin.__init__(
            self,
            text=text,
            parse_mode=parse_mode,
        )

    EDIT_INTO_ALLOWED = [
        SimpleMessage,
        PhotoMessage,
        VideoMessage,
        AudioMessage,
        DocumentMessage,
    ]

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        self.check_edit_into_message_type(new_message, self.EDIT_INTO_ALLOWED)
        if isinstance(new_message, SimpleMessage):
            message_id = await bot_adapter.edit_text(
                chat_id=self.user_id,
                message_id=self.message_id,
                text=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            )
            self.message_id = message_id
            self.text = new_message.text
            self.button_rows = new_message.button_rows

        elif isinstance(new_message, PhotoMessage):
            message_id = await bot_adapter.edit_message_media
            # TODO: доделать обработку других типов,
            # TODO: переделать BotAdapter, возможно сделать метод edit_message_media - универсальный


class SentMediaMessage(SentMessage, HasTextMixin):
    def __init__(
        self,
        *,
        text: str,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.category: MessageCategory = MessageCategory.MEDIA
        SentMessage.__init__(
            self,
            category=self.category,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
        )
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)

    def __new__(cls, *args, **kwargs):
        assert cls is not MediaMessage, (
            f"{cls.__name__} cannot be created directly, only its subclasses"
        )
        return super().__new__(cls)


class SentAudioMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        audio: Audio,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.audio = audio
        super().__init__(
            text=text,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )


class SentDocumentMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        document: Document,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.document = document
        super().__init__(
            text=text,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )


class SentPhotoMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        photo: Photo,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.photo = photo
        super().__init__(
            text=text,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )


class SentVideoMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        video: Video,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.video = video
        super().__init__(
            text=text,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )


class SentVideoNoteMessage(SentMessage):
    def __init__(
        self,
        message_id: int,
        user_id: int,
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(
            MessageCategory.VIDEO_NOTE,
            message_id=message_id,
            user_id=user_id,
            button_rows=button_rows,
        )
