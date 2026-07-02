import asyncio
from typing import Coroutine, Protocol

from tg_bot_screen.core.exceptions import (
    CannotTransformMessage,
    ImplementationError,
    MessageNotModified,
)
from tg_bot_screen.core.models.message import (
    AudioMessage,
    MessageCategory,
    PhotoMessage,
    SentAudioMessage,
    SentDocumentMessage,
    SentMessage,
    SentPhotoMessage,
    SentSimpleMessage,
    SimpleMessage,
    UnSentMessage,
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


# --------------------------------------------------------------------------- #


def get_edit_function(
    old_message: SentMessage,
    new_message: UnSentMessage,
) -> MessageEditFunc | None:
    old_category = old_message.category
    new_category = new_message.category

    strat = EditRegistrar.get_strategy(old_category, new_category)
    if strat is None:
        return

    checker = EditRegistrar.get_checker(old_category, new_category)

    if checker:
        result = checker(old_message, new_message)
        if result is None:
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
