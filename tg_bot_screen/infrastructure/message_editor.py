import asyncio
from typing import Any, Coroutine, Protocol, Sequence

from tg_bot_screen.core.exceptions import (
    CannotTransformMessage,
    ImplementationError,
    MessageNotModified,
)
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
    SimpleMessage,
    UnSentMessage,
    VideoMessage,
)
from tg_bot_screen.infrastructure.message_abstract_diff import (
    calc_abstract_difference_without_send,
)

from ..core.interfaces import BotAdapter, CallbackDataMapping, MessageEditor

# ----- #


async def run_parallel_requests(coroutines: list[Coroutine]) -> None:
    results = await asyncio.gather(*coroutines, return_exceptions=True)

    if all(isinstance(r, MessageNotModified) for r in results):
        raise MessageNotModified("All edits returned MessageNotModified")

    for result in results:
        if isinstance(result, Exception) and not isinstance(result, MessageNotModified):
            raise result

    return None


class MessageEditFunc(Protocol):
    async def __call__(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> SentMessage: ...


class EditChecker(Protocol):
    def __call__(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
    ) -> tuple[list[int], list[tuple[int, int]]] | None: ...


class EditRegistrar:
    _strategies: dict[tuple[MessageCategory, MessageCategory], MessageEditFunc] = {}
    _checker_funcs: dict[tuple[MessageCategory, MessageCategory], EditChecker] = {}

    @classmethod
    def register_strategy(cls, cat_from: MessageCategory, cat_to: MessageCategory):
        def wrapper(strategy: MessageEditFunc):
            cls._strategies[(cat_from, cat_to)] = strategy
            return strategy

        return wrapper

    @classmethod
    def get_strategy(cls, cat_from: MessageCategory, cat_to: MessageCategory):
        return cls._strategies.get((cat_from, cat_to))

    @classmethod
    def register_checker(cls, cat_from: MessageCategory, cat_to: MessageCategory):
        def wrapper(checker: EditChecker):
            cls._checker_funcs[(cat_from, cat_to)] = checker
            return checker

        return wrapper

    @classmethod
    def get_checker(cls, cat_from: MessageCategory, cat_to: MessageCategory):
        return cls._checker_funcs.get((cat_from, cat_to))


# --------------------------------------------------------------------------- #


@EditRegistrar.register_strategy(MessageCategory.SIMPLE, MessageCategory.SIMPLE)
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


# ----- #


@EditRegistrar.register_strategy(MessageCategory.SIMPLE, MessageCategory.PHOTO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentPhotoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.SIMPLE, MessageCategory.VIDEO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentVideoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.SIMPLE, MessageCategory.AUDIO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentAudioMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.SIMPLE, MessageCategory.DOCUMENT)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentDocumentMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


# ----- #


@EditRegistrar.register_strategy(MessageCategory.PHOTO, MessageCategory.PHOTO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentPhotoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.PHOTO, MessageCategory.VIDEO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentVideoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.PHOTO, MessageCategory.AUDIO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentAudioMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.PHOTO, MessageCategory.DOCUMENT)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentDocumentMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


# ----- #


@EditRegistrar.register_strategy(MessageCategory.VIDEO, MessageCategory.VIDEO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentVideoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.VIDEO, MessageCategory.PHOTO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentPhotoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.VIDEO, MessageCategory.AUDIO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentAudioMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.VIDEO, MessageCategory.DOCUMENT)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentDocumentMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


# ----- #


@EditRegistrar.register_strategy(MessageCategory.AUDIO, MessageCategory.AUDIO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentAudioMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.AUDIO, MessageCategory.PHOTO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentPhotoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.AUDIO, MessageCategory.VIDEO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentVideoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.AUDIO, MessageCategory.DOCUMENT)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentDocumentMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
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


@EditRegistrar.register_strategy(MessageCategory.DOCUMENT, MessageCategory.DOCUMENT)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentDocumentMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.DOCUMENT, MessageCategory.PHOTO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentPhotoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.DOCUMENT, MessageCategory.VIDEO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentVideoMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


@EditRegistrar.register_strategy(MessageCategory.DOCUMENT, MessageCategory.AUDIO)
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

    await bot_adapter.edit_message_media(
        chat_id=old_message.user_id,
        message_id=old_message.message_ids[0],
        media=new_message.media,
        mapping=mapping,
        button_rows=new_message.button_rows,
    )
    return SentAudioMessage(
        media=new_message.media,
        message_ids=old_message.message_ids,
        user_id=old_message.user_id,
        button_rows=new_message.button_rows,
    )


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


# --------------------------------------------------------------------------- #


def check_edit(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> tuple[list[int], list[tuple[int, int]]] | None:
    checker = EditRegistrar.get_checker(old_message.category, new_message.category)
    if checker is None:
        return None

    return checker(old_message, new_message)


def get_edit_function(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> MessageEditFunc | None:
    old_category = old_message.category
    new_category = new_message.category

    strat = EditRegistrar.get_strategy(old_category, new_category)
    if strat is None:
        return

    check_result = check_edit(old_message, new_message)
    if check_result is None:
        return None

    return strat


class MessageEditorImpl(MessageEditor):
    async def edit(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
        bot_adapter: BotAdapter,
        mapping: CallbackDataMapping,
    ) -> SentMessage:
        edit_func = get_edit_function(old_message, new_message)

        if edit_func is None:
            raise CannotTransformMessage(
                f"Cannot edit {old_message.category} to {new_message.category}"
            )

        return await edit_func(
            old_message,
            new_message,
            bot_adapter,
            mapping,
        )

    def check_message_can_be_replaced(
        self,
        old_message: SentMessage,
        new_message: UnSentMessage,
    ) -> bool:
        can_be = check_edit(old_message, new_message)
        if can_be is None:
            return False

        return True
