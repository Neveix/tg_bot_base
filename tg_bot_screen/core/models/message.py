from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Coroutine, Protocol, Self, Sequence

from tg_bot_screen.core.exceptions import (
    CannotTransformMessage,
    ImplementationError,
    MessageNotModified,
)
from tg_bot_screen.core.models.media_data import (
    Audio,
    Document,
    Photo,
    Video,
    VideoNote,
    Voice,
)
from tg_bot_screen.infrastructure.screen_abstract_diff import (
    calc_abstract_difference_without_send,
)

from ..interfaces import BotAdapter, CallbackData, CallbackDataMapping
from .button_rows import ButtonRows


class MessageCategory(StrEnum):
    SIMPLE = "simple"
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    PHOTO_VIDEO_ALBUM = "photo_video_album"
    DOCUMENT_ALBUM = "document_album"
    AUDIO_ALBUM = "audio_album"
    VOICE = "voice"
    VIDEO_NOTE = "video_note"


# ----- #


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


class UnSentMessage:
    def __init__(
        self,
        *,
        category: MessageCategory,
    ):
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


class SentMessage(ABC):
    def __init__(
        self,
        category: MessageCategory,
        message_ids: Sequence[int],
        user_id: int,
    ):
        self.category = category
        self.message_ids = message_ids
        self.user_id = user_id

    async def delete(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
    ):
        final_result = False
        for message_id in self.message_ids:
            result = await bot_adapter.delete_message(
                chat_id=user_id,
                message_id=message_id,
            )
            final_result |= result

        return final_result

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


# ----- #


class SimpleMessage(UnSentMessage, HasButtonRowsMixin, HasTextMixin):
    def __init__(
        self,
        text: str,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        UnSentMessage.__init__(
            self,
            category=MessageCategory.SIMPLE,
        )
        HasButtonRowsMixin.__init__(
            self,
            button_rows=button_rows,
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
            message_ids=[message_id],
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class MediaMessage(HasTextMixin, HasButtonRowsMixin):
    def __init__(
        self,
        *,
        text: str,
        category: MessageCategory,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.category = category
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)

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
        self.media = audio
        MediaMessage.__init__(
            self,
            text=text,
            category=MessageCategory.AUDIO,
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
            audio=self.media,
            text=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentAudioMessage(
            text=self.text,
            media=self.media,
            message_ids=[message_id],
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
        self.media = document
        MediaMessage.__init__(
            self,
            text=text,
            category=MessageCategory.DOCUMENT,
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
            document=self.media,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentDocumentMessage(
            text=self.text,
            media=self.media,
            message_ids=[message_id],
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
        self.media = photo
        MediaMessage.__init__(
            self,
            text=text,
            category=MessageCategory.PHOTO,
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
            photo=self.media,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentPhotoMessage(
            text=self.text,
            media=self.media,
            message_ids=[message_id],
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
        self.media = video
        MediaMessage.__init__(
            self,
            text=text,
            category=MessageCategory.VIDEO,
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
            video=self.media,
            caption=self.text,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentVideoMessage(
            text=self.text,
            media=self.media,
            message_ids=[message_id],
            user_id=user_id,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class VoiceMessage(HasButtonRowsMixin, UnSentMessage):
    def __init__(
        self,
        voice: Voice,
        button_rows: ButtonRows | None = None,
    ):
        self.voice = voice
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        UnSentMessage.__init__(self, category=MessageCategory.VOICE)

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_id = await bot_adapter.send_voice(
            chat_id=user_id,
            voice=self.voice,
            mapping=mapping,
            button_rows=self.button_rows,
        )

        return SentVoiceMessage(
            voice=self.voice,
            message_ids=[message_id],
            user_id=user_id,
            button_rows=self.button_rows,
        )


class VideoNoteMessage(HasButtonRowsMixin, UnSentMessage):
    def __init__(
        self,
        video_note: VideoNote,
        button_rows: ButtonRows | None = None,
    ):
        self.video_note = video_note
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        UnSentMessage.__init__(self, category=MessageCategory.VIDEO_NOTE)

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
            video_note=self.video_note,
            message_ids=[message_id],
            user_id=user_id,
            button_rows=self.button_rows,
        )


class PhotoVideoAlbumMessage(HasTextMixin, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Sequence[Photo | Video],
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(
            self,
            text=text,
            parse_mode=parse_mode,
        )
        UnSentMessage.__init__(
            self,
            category=MessageCategory.PHOTO_VIDEO_ALBUM,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_ids = await bot_adapter.send_media_group(
            chat_id=user_id,
            media=self.media,
            caption=self.text,
            mapping=mapping,
        )

        return SentPhotoVideoAlbumMessage(
            text=self.text,
            media=self.media,
            message_ids=message_ids,
            user_id=user_id,
            parse_mode=self.parse_mode,
        )


class AudioAlbumMessage(HasTextMixin, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Sequence[Audio],
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(
            self,
            text=text,
            parse_mode=parse_mode,
        )
        UnSentMessage.__init__(
            self,
            category=MessageCategory.AUDIO_ALBUM,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_ids = await bot_adapter.send_media_group(
            chat_id=user_id,
            media=self.media,
            caption=self.text,
            mapping=mapping,
        )

        return SentAudioAlbumMessage(
            text=self.text,
            media=self.media,
            message_ids=message_ids,
            user_id=user_id,
            parse_mode=self.parse_mode,
        )


class DocumentAlbumMessage(HasTextMixin, UnSentMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Sequence[Document],
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(
            self,
            text=text,
            parse_mode=parse_mode,
        )
        UnSentMessage.__init__(
            self,
            category=MessageCategory.DOCUMENT_ALBUM,
        )

    async def send(
        self,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ):
        message_ids = await bot_adapter.send_media_group(
            chat_id=user_id,
            media=self.media,
            caption=self.text,
            mapping=mapping,
        )

        return SentDocumentAlbumMessage(
            text=self.text,
            media=self.media,
            message_ids=message_ids,
            user_id=user_id,
            parse_mode=self.parse_mode,
        )


# ----- #


async def run_parallel_requests(coroutines: list[Coroutine]) -> None:
    results = await asyncio.gather(*coroutines, return_exceptions=True)

    if all(isinstance(r, MessageNotModified) for r in results):
        raise MessageNotModified("All edits returned MessageNotModified")

    for result in results:
        if isinstance(result, Exception) and not isinstance(result, MessageNotModified):
            raise result

    return None


class SentSimpleMessage(SentMessage, HasButtonRowsMixin, HasTextMixin):
    def __init__(
        self,
        text: str,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        SentMessage.__init__(
            self,
            category=MessageCategory.SIMPLE,
            message_ids=message_ids,
            user_id=user_id,
        )
        HasButtonRowsMixin.__init__(
            self,
            button_rows=button_rows,
        )
        HasTextMixin.__init__(
            self,
            text=text,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return SimpleMessage(
            text=self.text,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentMediaMessage(SentMessage, HasButtonRowsMixin, HasTextMixin):
    def __init__(
        self,
        *,
        text: str,
        message_ids: Sequence[int],
        user_id: int,
        category: MessageCategory,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        SentMessage.__init__(
            self,
            category=category,
            message_ids=message_ids,
            user_id=user_id,
        )
        HasButtonRowsMixin.__init__(
            self,
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
        media: Audio,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.audio = media
        super().__init__(
            text=text,
            message_ids=message_ids,
            category=MessageCategory.AUDIO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return AudioMessage(
            text=self.text,
            audio=self.audio,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentDocumentMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Document,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.document = media
        super().__init__(
            text=text,
            message_ids=message_ids,
            user_id=user_id,
            category=MessageCategory.DOCUMENT,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return DocumentMessage(
            text=self.text,
            document=self.document,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentPhotoMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Photo,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.photo = media
        super().__init__(
            text=text,
            message_ids=message_ids,
            category=MessageCategory.PHOTO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return PhotoMessage(
            text=self.text,
            photo=self.photo,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentVideoMessage(SentMediaMessage):
    def __init__(
        self,
        *,
        text: str,
        media: Video,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.video = media
        super().__init__(
            text=text,
            message_ids=message_ids,
            category=MessageCategory.VIDEO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return VideoMessage(
            text=self.text,
            video=self.video,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentVoiceMessage(HasButtonRowsMixin, SentMessage):
    def __init__(
        self,
        voice: Voice,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
    ):
        self.voice = voice
        SentMessage.__init__(
            self,
            category=MessageCategory.VOICE,
            message_ids=message_ids,
            user_id=user_id,
        )
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)

    def get_unsent(self) -> UnSentMessage:
        return VoiceMessage(
            voice=self.voice,
            button_rows=self.button_rows,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        raise CannotTransformMessage(
            f"{type(self)} cannot be transformed into {type(new_message)}"
        )


class SentVideoNoteMessage(HasButtonRowsMixin, SentMessage):
    def __init__(
        self,
        video_note: VideoNote,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
    ):
        self.video_note = video_note
        SentMessage.__init__(
            self,
            category=MessageCategory.VIDEO_NOTE,
            message_ids=message_ids,
            user_id=user_id,
        )
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)

    def get_unsent(self) -> UnSentMessage:
        return VideoNoteMessage(
            video_note=self.video_note,
            button_rows=self.button_rows,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        raise CannotTransformMessage(
            f"{type(self)} cannot be transformed into {type(new_message)}"
        )


class SentPhotoVideoAlbumMessage(HasTextMixin, SentMessage):
    def __init__(
        self,
        text: str,
        media: Sequence[Photo | Video],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)
        SentMessage.__init__(
            self,
            category=MessageCategory.PHOTO_VIDEO_ALBUM,
            message_ids=message_ids,
            user_id=user_id,
        )

    def get_unsent(self) -> UnSentMessage:
        return PhotoVideoAlbumMessage(
            text=self.text,
            media=self.media,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentAudioAlbumMessage(HasTextMixin, SentMessage):
    def __init__(
        self,
        text: str,
        media: Sequence[Audio],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)
        SentMessage.__init__(
            self,
            category=MessageCategory.AUDIO_ALBUM,
            message_ids=message_ids,
            user_id=user_id,
        )

    def get_unsent(self) -> UnSentMessage:
        return AudioAlbumMessage(
            text=self.text,
            media=self.media,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


class SentDocumentAlbumMessage(HasTextMixin, SentMessage):
    def __init__(
        self,
        text: str,
        media: Sequence[Document],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text, parse_mode=parse_mode)
        SentMessage.__init__(
            self,
            category=MessageCategory.DOCUMENT_ALBUM,
            message_ids=message_ids,
            user_id=user_id,
        )

    def get_unsent(self) -> UnSentMessage:
        return DocumentAlbumMessage(
            text=self.text,
            media=self.media,
            parse_mode=self.parse_mode,
        )

    async def edit(
        self,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> Self:
        # TODO:
        ...


# --------------------------------------------------------------------------- #


class MessageEditFunc(Protocol):
    async def __call__(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> SentMessage: ...


class MessageCanBeEditerFunc(Protocol):
    def __call__(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
    ) -> tuple[list[int], list[tuple[int, int]]] | None: ...


# ----- #


async def edit_simple_to_simple(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentSimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, SimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await bot_adapter.edit_message_text(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        text=new_message.text,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentSimpleMessage(
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_simple_to_photo(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentSimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentPhotoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_simple_to_video(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentSimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, VideoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentVideoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_simple_to_audio(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentSimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentAudioMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_simple_to_document(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentSimpleMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentDocumentMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


# ----- #


async def edit_photo_to_photo(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentPhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentPhotoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_photo_to_video(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentPhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, VideoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentVideoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_photo_to_audio(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentPhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentAudioMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_photo_to_document(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentPhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentDocumentMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


# ----- #


async def edit_video_to_video(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentVideoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, VideoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentVideoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_video_to_photo(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentVideoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentPhotoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_video_to_audio(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentVideoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentAudioMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_video_to_document(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentVideoMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentDocumentMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


# ----- #


async def edit_audio_to_audio(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentAudioMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentAudioMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_audio_to_photo(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentAudioMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentPhotoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_audio_to_video(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentAudioMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, VideoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentVideoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_audio_to_document(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentAudioMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentDocumentMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


# ----- #


async def edit_document_to_document(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentDocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentDocumentMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_document_to_photo(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentDocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentPhotoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_document_to_video(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentDocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, VideoMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentVideoMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


async def edit_document_to_audio(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentDocumentMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    await run_parallel_requests(
        [
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                media=new_message.media,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
            bot_adapter.edit_message_caption(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[0],
                caption=new_message.text,
                mapping=mapping,
                button_rows=new_message.button_rows,
            ),
        ]
    )
    return SentAudioMessage(
        media=new_message.media,
        text=new_message.text,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
        parse_mode=old_message.parse_mode,
    )


# ----- #


def get_message_media_types(media: Sequence[Any]) -> dict[Any, int]:
    type_codes = []
    for media_obj in media:
        type_codes.append(media_obj)
    return {code: i for i, code in enumerate(type_codes)}


class AlbumMessage(Protocol):
    media: Sequence[Any]


def calc_message_difference_without_send(
    old_message: AlbumMessage, new_message: AlbumMessage
) -> tuple[list[int], list[tuple[int, int]]] | None:
    types = get_message_media_types(*old_message.media, *new_message.media)
    old_types = [types[media] for media in old_message.media]

    new_types = [types[media] for media in new_message.media]
    return calc_abstract_difference_without_send(old_types, new_types)


# ----- #


def photo_video_album_can_be_edited(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> tuple[list[int], list[tuple[int, int]]] | None:
    if not isinstance(old_message, SentPhotoVideoAlbumMessage):
        return

    if not isinstance(new_message, PhotoVideoAlbumMessage):
        return

    return calc_message_difference_without_send(old_message, new_message)


async def edit_photo_video_album_to_photo_video_album(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentPhotoVideoAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, PhotoVideoAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    edit_plan = photo_video_album_can_be_edited(old_message, new_message)
    if edit_plan is None:
        raise CannotTransformMessage(
            "Cannot edit photo/video album: new media count exceeds old media count"
        )

    indices_to_delete, indices_to_edit = edit_plan

    tasks = []

    for idx in indices_to_delete:
        tasks.append(
            bot_adapter.delete_message(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[idx],
            )
        )

    for old_idx, new_idx in indices_to_edit:
        new_media = new_message.media[new_idx]
        tasks.append(
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[old_idx],
                media=new_media,
                mapping=mapping,
            )
        )

    await run_parallel_requests(tasks)

    new_message_ids = []
    for old_idx, new_idx in indices_to_edit:
        new_message_ids.append(old_message.message_ids[old_idx])

    return SentPhotoVideoAlbumMessage(
        text=new_message.text,
        media=new_message.media,
        message_ids=new_message_ids,
        user_id=old_message.user_id,
        parse_mode=new_message.parse_mode,
    )


# ----- #


def audio_album_can_be_edited(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> tuple[list[int], list[tuple[int, int]]] | None:
    if not isinstance(old_message, SentAudioAlbumMessage):
        return None

    if not isinstance(new_message, AudioAlbumMessage):
        return None

    old_audio_count = len(old_message.media)
    new_audio_count = len(new_message.media)

    if new_audio_count > old_audio_count:
        return None

    indices_delete = list(range(new_audio_count, old_audio_count))
    indices_edit = [(i, i) for i in range(new_audio_count)]

    return indices_delete, indices_edit


async def edit_audio_album_to_audio_album(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentAudioAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, AudioAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    edit_plan = audio_album_can_be_edited(old_message, new_message)
    if edit_plan is None:
        raise CannotTransformMessage(
            "Cannot edit audio album: new audio count exceeds old audio count"
        )

    indices_to_delete, indices_to_edit = edit_plan

    tasks = []

    for idx in indices_to_delete:
        tasks.append(
            bot_adapter.delete_message(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[idx],
            )
        )

    for old_idx, new_idx in indices_to_edit:
        new_audio = new_message.media[new_idx]
        tasks.append(
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[old_idx],
                media=new_audio,
                mapping=mapping,
            )
        )

    await run_parallel_requests(tasks)

    new_message_ids = []
    for old_idx, new_idx in indices_to_edit:
        new_message_ids.append(old_message.message_ids[old_idx])

    return SentAudioAlbumMessage(
        text=new_message.text,
        media=new_message.media,
        message_ids=new_message_ids,
        user_id=old_message.user_id,
        parse_mode=new_message.parse_mode,
    )


# ----- #


def document_album_can_be_edited(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> tuple[list[int], list[tuple[int, int]]] | None:
    if not isinstance(old_message, SentDocumentAlbumMessage):
        return None

    if not isinstance(new_message, DocumentAlbumMessage):
        return None

    old_document_count = len(old_message.media)
    new_document_count = len(new_message.media)

    if new_document_count > old_document_count:
        return None

    indices_delete = list(range(new_document_count, old_document_count))
    indices_edit = [(i, i) for i in range(new_document_count)]

    return indices_delete, indices_edit


async def edit_document_album_to_document_album(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(old_message, SentDocumentAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(old_message).__name__}")
    if not isinstance(new_message, DocumentAlbumMessage):
        raise ImplementationError(f"Found unexpected type {type(new_message).__name__}")

    edit_plan = document_album_can_be_edited(old_message, new_message)
    if edit_plan is None:
        raise CannotTransformMessage(
            "Cannot edit document album: new document count exceeds old document count"
        )

    indices_to_delete, indices_to_edit = edit_plan

    tasks = []

    for idx in indices_to_delete:
        tasks.append(
            bot_adapter.delete_message(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[idx],
            )
        )

    for old_idx, new_idx in indices_to_edit:
        new_document = new_message.media[new_idx]
        tasks.append(
            bot_adapter.edit_message_media(
                chat_id=old_message.user_id,
                message_id=old_message.message_ids[old_idx],
                media=new_document,
                mapping=mapping,
            )
        )

    await run_parallel_requests(tasks)

    new_message_ids = []
    for old_idx, new_idx in indices_to_edit:
        new_message_ids.append(old_message.message_ids[old_idx])

    return SentDocumentAlbumMessage(
        text=new_message.text,
        media=new_message.media,
        message_ids=new_message_ids,
        user_id=old_message.user_id,
        parse_mode=new_message.parse_mode,
    )


# ----- #


EDIT_MEDIA_MATRIX: dict[
    MessageCategory,
    dict[
        MessageCategory,
        MessageEditFunc | tuple[MessageEditFunc, MessageCanBeEditerFunc],
    ],
] = {
    MessageCategory.SIMPLE: {
        MessageCategory.SIMPLE: edit_simple_to_simple,
        MessageCategory.PHOTO: edit_simple_to_photo,
        MessageCategory.VIDEO: edit_simple_to_video,
        MessageCategory.AUDIO: edit_simple_to_audio,
        MessageCategory.DOCUMENT: edit_simple_to_document,
    },
    MessageCategory.PHOTO: {
        MessageCategory.PHOTO: edit_photo_to_photo,
        MessageCategory.VIDEO: edit_photo_to_video,
        MessageCategory.AUDIO: edit_photo_to_audio,
        MessageCategory.DOCUMENT: edit_photo_to_document,
    },
    MessageCategory.VIDEO: {
        MessageCategory.VIDEO: edit_video_to_video,
        MessageCategory.PHOTO: edit_video_to_photo,
        MessageCategory.AUDIO: edit_video_to_audio,
        MessageCategory.DOCUMENT: edit_video_to_document,
    },
    MessageCategory.AUDIO: {
        MessageCategory.AUDIO: edit_audio_to_audio,
        MessageCategory.PHOTO: edit_audio_to_photo,
        MessageCategory.VIDEO: edit_audio_to_video,
        MessageCategory.DOCUMENT: edit_audio_to_document,
    },
    MessageCategory.DOCUMENT: {
        MessageCategory.DOCUMENT: edit_document_to_document,
        MessageCategory.PHOTO: edit_document_to_photo,
        MessageCategory.VIDEO: edit_document_to_video,
        MessageCategory.AUDIO: edit_document_to_audio,
    },
    MessageCategory.PHOTO_VIDEO_ALBUM: {
        MessageCategory.PHOTO_VIDEO_ALBUM: (
            edit_photo_video_album_to_photo_video_album,
            photo_video_album_can_be_edited,
        )
    },
    MessageCategory.DOCUMENT_ALBUM: {
        MessageCategory.DOCUMENT_ALBUM: (
            edit_document_album_to_document_album,
            photo_video_album_can_be_edited,
        )
    },
    MessageCategory.AUDIO_ALBUM: {
        MessageCategory.AUDIO_ALBUM: (
            edit_audio_album_to_audio_album,
            photo_video_album_can_be_edited,
        )
    },
}


def get_edit_function(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> MessageEditFunc | None:
    old_category = old_message.category
    new_category = new_message.category

    if old_category not in EDIT_MEDIA_MATRIX:
        return None

    if new_category not in EDIT_MEDIA_MATRIX[old_category]:
        return None

    entry = EDIT_MEDIA_MATRIX[old_category][new_category]

    if isinstance(entry, tuple):
        edit_func, checker_func = entry
        result = checker_func(old_message, new_message)
        if result is None:
            return None
        return edit_func

    return entry


async def universal_edit(
    old_message: SentMessage,
    new_message: UnSentMessage,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    edit_func = get_edit_function(old_message, new_message)

    if edit_func is None:
        raise CannotTransformMessage(
            f"Cannot transform from {old_message.category} to {new_message.category}"
        )

    return await edit_func(old_message, new_message, bot_adapter, mapping)
