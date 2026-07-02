from typing import Protocol

from tg_bot_screen.core.exceptions import ImplementationError
from tg_bot_screen.core.models.message import (
    AudioAlbumMessage,
    AudioMessage,
    DocumentAlbumMessage,
    DocumentMessage,
    MessageCategory,
    PhotoMessage,
    PhotoVideoAlbumMessage,
    SentAudioAlbumMessage,
    SentAudioMessage,
    SentDocumentAlbumMessage,
    SentDocumentMessage,
    SentMessage,
    SentPhotoMessage,
    SentPhotoVideoAlbumMessage,
    SentSimpleMessage,
    SentVideoMessage,
    SentVideoNoteMessage,
    SentVoiceMessage,
    SimpleMessage,
    UnSentMessage,
    VideoMessage,
    VideoNoteMessage,
    VoiceMessage,
)

from ..core.interfaces import BotAdapter, CallbackDataMapping, MessageSender


class SendFunc(Protocol):
    async def __call__(
        self,
        message: UnSentMessage,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> SentMessage: ...


class SendRegistrar:
    _strategies: dict[MessageCategory, SendFunc] = {}

    @classmethod
    def register(cls, category: MessageCategory):
        def wrapper(func: SendFunc):
            cls._strategies[category] = func
            return func

        return wrapper

    @classmethod
    def get(cls, category: MessageCategory):
        return cls._strategies.get(category)


# ----- #


@SendRegistrar.register(MessageCategory.SIMPLE)
async def send_simple(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, SimpleMessage):
        raise ImplementationError(
            f"Expected SimpleMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_message(
        chat_id=user_id,
        text=message.text,
        mapping=mapping,
        parse_mode=message.parse_mode,
        button_rows=message.button_rows,
    )

    return SentSimpleMessage(
        text=message.text,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.AUDIO)
async def send_audio(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, AudioMessage):
        raise ImplementationError(
            f"Expected AudioMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_audio(
        chat_id=user_id,
        audio=message.media,
        text=message.text,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentAudioMessage(
        text=message.text,
        media=message.media,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.DOCUMENT)
async def send_document(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, DocumentMessage):
        raise ImplementationError(
            f"Expected DocumentMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_document(
        chat_id=user_id,
        document=message.media,
        caption=message.text,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentDocumentMessage(
        text=message.text,
        media=message.media,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.PHOTO)
async def send_photo(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, PhotoMessage):
        raise ImplementationError(
            f"Expected PhotoMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_photo(
        chat_id=user_id,
        photo=message.media,
        caption=message.text,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentPhotoMessage(
        text=message.text,
        media=message.media,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.VIDEO)
async def send_video(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, VideoMessage):
        raise ImplementationError(
            f"Expected VideoMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_video(
        chat_id=user_id,
        video=message.media,
        caption=message.text,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentVideoMessage(
        text=message.text,
        media=message.media,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.VOICE)
async def send_voice(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, VoiceMessage):
        raise ImplementationError(
            f"Expected VoiceMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_voice(
        chat_id=user_id,
        voice=message.voice,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentVoiceMessage(
        voice=message.voice,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
    )


@SendRegistrar.register(MessageCategory.VIDEO_NOTE)
async def send_video_note(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, VideoNoteMessage):
        raise ImplementationError(
            f"Expected VideoNoteMessage, got {type(message).__name__}"
        )

    message_id = await bot_adapter.send_video_note(
        chat_id=user_id,
        video_note=message.video_note,
        mapping=mapping,
        button_rows=message.button_rows,
    )

    return SentVideoNoteMessage(
        video_note=message.video_note,
        message_ids=[message_id],
        user_id=user_id,
        button_rows=message.button_rows,
    )


@SendRegistrar.register(MessageCategory.PHOTO_VIDEO_ALBUM)
async def send_photo_video_album(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, PhotoVideoAlbumMessage):
        raise ImplementationError(
            f"Expected PhotoVideoAlbumMessage, got {type(message).__name__}"
        )

    message_ids = await bot_adapter.send_media_group(
        chat_id=user_id,
        media=message.media,
        caption=message.text,
        mapping=mapping,
    )

    return SentPhotoVideoAlbumMessage(
        text=message.text,
        media=message.media,
        message_ids=message_ids,
        user_id=user_id,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.AUDIO_ALBUM)
async def send_audio_album(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, AudioAlbumMessage):
        raise ImplementationError(
            f"Expected AudioAlbumMessage, got {type(message).__name__}"
        )

    message_ids = await bot_adapter.send_media_group(
        chat_id=user_id,
        media=message.media,
        caption=message.text,
        mapping=mapping,
    )

    return SentAudioAlbumMessage(
        text=message.text,
        media=message.media,
        message_ids=message_ids,
        user_id=user_id,
        parse_mode=message.parse_mode,
    )


@SendRegistrar.register(MessageCategory.DOCUMENT_ALBUM)
async def send_document_album(
    message: UnSentMessage,
    user_id: int,
    bot_adapter: BotAdapter,
    mapping: CallbackDataMapping,
) -> SentMessage:
    if not isinstance(message, DocumentAlbumMessage):
        raise ImplementationError(
            f"Expected DocumentAlbumMessage, got {type(message).__name__}"
        )

    message_ids = await bot_adapter.send_media_group(
        chat_id=user_id,
        media=message.media,
        caption=message.text,
        mapping=mapping,
    )

    return SentDocumentAlbumMessage(
        text=message.text,
        media=message.media,
        message_ids=message_ids,
        user_id=user_id,
        parse_mode=message.parse_mode,
    )


# ----- #


class MessageSenderImpl(MessageSender):
    async def send(
        self,
        message: UnSentMessage,
        user_id: int,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> SentMessage:
        if func := SendRegistrar.get(message.category):
            return await func(message, user_id, bot_adapter, mapping)

        raise ImplementationError(
            f"send function is not implemented for {message.category}"
        )
