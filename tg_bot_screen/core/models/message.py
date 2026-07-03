from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Self, Sequence

from tg_bot_screen.core.models.media_data import (
    Audio,
    Document,
    Photo,
    Video,
    VideoNote,
    Voice,
)

from .callback_data import CallbackData
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


@dataclass(kw_only=True)
class HasParseModeMixin:
    parse_mode: ParseMode | None = None


@dataclass(kw_only=True)
class HasButtonRowsMixin:
    button_rows: ButtonRows | None = None

    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()


class UnSentMessage(ABC):
    def __init__(
        self,
        *,
        category: MessageCategory,
    ):
        self.category = category

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

    @abstractmethod
    def get_unsent(self) -> UnSentMessage: ...


Message = UnSentMessage | SentMessage


# ----- #


class MediaMessage(HasButtonRowsMixin, HasParseModeMixin):
    def __init__(
        self,
        *,
        category: MessageCategory,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.category = category
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)

    def __new__(cls, *args, **kwargs):
        assert cls is not MediaMessage, (
            f"{cls.__name__} cannot be created directly, only its subclasses"
        )
        return super().__new__(cls)


class SimpleMessage(UnSentMessage, HasButtonRowsMixin, HasTextMixin, HasParseModeMixin):
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
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)

    def clone(self) -> Self:
        return type(self)(
            text=self.text,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class AudioMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        audio: Audio,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = audio
        MediaMessage.__init__(
            self,
            category=MessageCategory.AUDIO,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def clone(self) -> Self:
        return type(self)(
            audio=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class DocumentMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        document: Document,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = document
        MediaMessage.__init__(
            self,
            category=MessageCategory.DOCUMENT,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def clone(self) -> Self:
        return type(self)(
            document=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class PhotoMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        photo: Photo,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = photo
        MediaMessage.__init__(
            self,
            category=MessageCategory.PHOTO,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def clone(self) -> Self:
        return type(self)(
            photo=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class VideoMessage(MediaMessage, UnSentMessage):
    def __init__(
        self,
        video: Video,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = video
        MediaMessage.__init__(
            self,
            category=MessageCategory.VIDEO,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def clone(self) -> Self:
        return type(self)(
            video=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class VoiceMessage(HasButtonRowsMixin, HasParseModeMixin, UnSentMessage):
    def __init__(
        self,
        voice: Voice,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.voice = voice
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
        UnSentMessage.__init__(self, category=MessageCategory.VOICE)

    def clone(self) -> Self:
        return type(self)(
            voice=self.voice,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
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

    def clone(self) -> Self:
        return type(self)(
            video_note=self.video_note,
            button_rows=self.button_rows,
        )


class PhotoVideoAlbumMessage(UnSentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Photo | Video],
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        self.button_rows = button_rows
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
        UnSentMessage.__init__(
            self,
            category=MessageCategory.PHOTO_VIDEO_ALBUM,
        )

    def clone(self) -> Self:
        return type(self)(
            text=self.text,
            media=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class AudioAlbumMessage(UnSentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Audio],
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        self.button_rows = button_rows
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
        UnSentMessage.__init__(
            self,
            category=MessageCategory.AUDIO_ALBUM,
        )

    def clone(self) -> Self:
        return type(self)(
            text=self.text,
            media=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class DocumentAlbumMessage(UnSentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Document],
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        self.button_rows = button_rows
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
        UnSentMessage.__init__(
            self,
            category=MessageCategory.DOCUMENT_ALBUM,
        )

    def clone(self) -> Self:
        return type(self)(
            text=self.text,
            media=self.media,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


# ----- #


class SentSimpleMessage(
    SentMessage, HasButtonRowsMixin, HasTextMixin, HasParseModeMixin
):
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
        )
        HasParseModeMixin.__init__(
            self,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return SimpleMessage(
            text=self.text,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class SentMediaMessage(SentMessage, HasButtonRowsMixin, HasParseModeMixin):
    def __init__(
        self,
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
        HasParseModeMixin.__init__(
            self,
            parse_mode=parse_mode,
        )

    def __new__(cls, *args, **kwargs):
        assert cls is not SentMediaMessage, (
            f"{cls.__name__} cannot be created directly, only its subclasses"
        )
        return super().__new__(cls)


class SentAudioMessage(SentMediaMessage):
    def __init__(
        self,
        media: Audio,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.audio = media
        super().__init__(
            message_ids=message_ids,
            category=MessageCategory.AUDIO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return AudioMessage(
            audio=self.audio,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class SentDocumentMessage(SentMediaMessage):
    def __init__(
        self,
        media: Document,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.document = media
        super().__init__(
            message_ids=message_ids,
            user_id=user_id,
            category=MessageCategory.DOCUMENT,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return DocumentMessage(
            document=self.document,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class SentPhotoMessage(SentMediaMessage):
    def __init__(
        self,
        media: Photo,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.photo = media
        super().__init__(
            message_ids=message_ids,
            category=MessageCategory.PHOTO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return PhotoMessage(
            photo=self.photo,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class SentVideoMessage(SentMediaMessage):
    def __init__(
        self,
        media: Video,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.video = media
        super().__init__(
            message_ids=message_ids,
            category=MessageCategory.VIDEO,
            user_id=user_id,
            button_rows=button_rows,
            parse_mode=parse_mode,
        )

    def get_unsent(self) -> UnSentMessage:
        return VideoMessage(
            video=self.video,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
        )


class SentVoiceMessage(HasButtonRowsMixin, HasParseModeMixin, SentMessage):
    def __init__(
        self,
        voice: Voice,
        message_ids: Sequence[int],
        user_id: int,
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        self.voice = voice
        SentMessage.__init__(
            self,
            category=MessageCategory.VOICE,
            message_ids=message_ids,
            user_id=user_id,
        )
        HasButtonRowsMixin.__init__(self, button_rows=button_rows)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)

    def get_unsent(self) -> UnSentMessage:
        return VoiceMessage(
            voice=self.voice,
            button_rows=self.button_rows,
            parse_mode=self.parse_mode,
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


class SentPhotoVideoAlbumMessage(SentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Photo | Video],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
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


class SentAudioAlbumMessage(SentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Audio],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
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


class SentDocumentAlbumMessage(SentMessage, HasTextMixin, HasParseModeMixin):
    def __init__(
        self,
        text: str,
        media: Sequence[Document],
        message_ids: Sequence[int],
        user_id: int,
        parse_mode: ParseMode | None = None,
    ):
        self.media = media
        HasTextMixin.__init__(self, text=text)
        HasParseModeMixin.__init__(self, parse_mode=parse_mode)
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


# --------------------------------------------------------------------------- #
