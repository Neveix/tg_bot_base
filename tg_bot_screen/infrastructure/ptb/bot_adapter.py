from typing import Sequence

from telegram import Bot
from telegram.error import BadRequest as PtbBadRequest

from tg_bot_screen.core.models.media_data import (
    Audio,
    Document,
    Photo,
    Video,
    VideoNote,
    Voice,
)
from .media_converter import (
    GeneralConverterPtb,
)

from ...core.models.button_rows import ButtonRows
from ...core.interfaces import (
    BotAdapter,
    ButtonRowsToReplyMarkupConverter,
    CallbackDataMapping,
)
from ...core.exceptions import (
    TgBotScreenException,
    MessageNotModified,
    BadRequest,
)


def get_wrapped_error(error: Exception) -> Exception:
    if isinstance(error, TgBotScreenException):
        raise

    if isinstance(error, PtbBadRequest):
        error_text = str(error).lower()
        if "message is not modified" in error_text:
            return MessageNotModified(str(error))
        return BadRequest(str(error))
    return TgBotScreenException(str(error))


class BotAdapterPtb(BotAdapter):
    def __init__(
        self,
        bot: Bot,
        button_rows_converter: ButtonRowsToReplyMarkupConverter,
        general_converter: GeneralConverterPtb | None = None,
    ):
        self.bot = bot
        self.button_rows_converter = button_rows_converter
        self.general_converter = general_converter or GeneralConverterPtb()

    def _prepare_reply_markup(
        self,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None,
    ):
        return self.button_rows_converter.convert(mapping, button_rows)

    async def send_message(
        self,
        chat_id: int,
        text: str,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            msg = await self.bot.send_message(
                chat_id,
                text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return msg.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_audio(
        self,
        chat_id: int,
        text: str,
        audio: Audio,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            msg = await self.bot.send_audio(
                chat_id,
                self.general_converter.to_send_parameter(audio),
                parse_mode=parse_mode,
                caption=text,
                reply_markup=reply_markup,
            )
            return msg.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_photo(
        self,
        chat_id: int,
        photo: Photo,
        caption: str,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_photo(
                chat_id,
                self.general_converter.to_send_parameter(photo),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_video(
        self,
        chat_id: int,
        video: Video,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_video(
                chat_id,
                self.general_converter.to_send_parameter(video),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_document(
        self,
        chat_id: int,
        document: Document,
        caption: str | None,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_document(
                chat_id,
                self.general_converter.to_send_parameter(document),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_voice(
        self,
        chat_id: int,
        voice: Voice,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_voice(
                chat_id,
                self.general_converter.to_send_parameter(voice),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_video_note(
        self,
        chat_id: int,
        video_note: VideoNote,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_video_note(
                chat_id,
                self.general_converter.to_send_parameter(video_note),
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def send_media_group(
        self,
        chat_id: int,
        media: Sequence[Photo | Video | Audio | Document],
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
    ) -> list[int]:
        try:
            result = await self.bot.send_media_group(
                chat_id=chat_id,
                media=[self.general_converter.to_input_media(m) for m in media],
            )
            return [msg.message_id for msg in result]
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def delete_message(self, chat_id: int, message_id: int) -> bool:
        try:
            result = await self.bot.delete_message(chat_id, message_id)
            return result
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def edit_message_text(
        self,
        chat_id: int,
        message_id: int,
        text: str,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.edit_message_text(
                text, chat_id, message_id, reply_markup=reply_markup
            )
            if isinstance(result, bool):
                raise ValueError(f"result of an edited message is {result=}")
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def edit_message_media(
        self,
        chat_id: int,
        message_id: int,
        media: Photo | Video | Audio | Document,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            converted_media = self.general_converter.to_input_media(media)
            result = await self.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=converted_media,
                reply_markup=reply_markup,
            )
            if isinstance(result, bool):
                raise ValueError("edit_message_media returned bool, expected Message")
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e

    async def edit_message_caption(
        self,
        chat_id: int,
        message_id: int,
        caption: str | None,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            if isinstance(result, bool):
                raise ValueError("edit_message_caption returned bool, expected Message")
            return result.message_id
        except Exception as e:
            raise get_wrapped_error(e) from e
