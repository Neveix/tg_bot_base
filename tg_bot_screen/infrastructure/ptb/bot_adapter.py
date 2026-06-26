import asyncio

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
    AudioConverterPtb,
    DocumentConverterPtb,
    PhotoConverterPtb,
    VideoConverterPtb,
    VideoNoteConverterPtb,
    VoiceConverterPtb,
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


def get_ptb_error(error: Exception) -> Exception:
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
        audio_converter: AudioConverterPtb | None = None,
        document_converter: DocumentConverterPtb | None = None,
        photo_converter: PhotoConverterPtb | None = None,
        voice_converter: VoiceConverterPtb | None = None,
        video_converter: VideoConverterPtb | None = None,
        video_note_converter: VideoNoteConverterPtb | None = None,
    ):
        self.bot = bot
        self.button_rows_converter = button_rows_converter
        self.audio_converter = audio_converter or AudioConverterPtb()
        self.document_converter = document_converter or DocumentConverterPtb()
        self.photo_converter = photo_converter or PhotoConverterPtb()
        self.voice_converter = voice_converter or VoiceConverterPtb()
        self.video_converter = video_converter or VideoConverterPtb()
        self.video_note_converter = video_note_converter or VideoNoteConverterPtb()

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
            raise get_ptb_error(e) from e

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
                self.audio_converter.convert(audio),
                parse_mode=parse_mode,
                caption=text,
                reply_markup=reply_markup,
            )
            return msg.message_id
        except Exception as e:
            raise get_ptb_error(e) from e

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
                self.photo_converter.convert(photo),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_ptb_error(e) from e

    async def send_video(
        self,
        chat_id: int,
        video: Video,
        caption: str,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_video(
                chat_id,
                self.video_converter.convert(video),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_ptb_error(e) from e

    async def send_document(
        self,
        chat_id: int,
        document: Document,
        caption: str,
        mapping: CallbackDataMapping,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)
            result = await self.bot.send_document(
                chat_id,
                self.document_converter.convert(document),
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_ptb_error(e) from e

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
                self.video_note_converter.convert(video_note),
                reply_markup=reply_markup,
            )
            return result.message_id
        except Exception as e:
            raise get_ptb_error(e) from e

    async def delete_message(self, chat_id: int, message_id: int) -> bool:
        try:
            result = await self.bot.delete_message(chat_id, message_id)
            return result
        except Exception as e:
            raise get_ptb_error(e) from e

    async def edit_text(
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
            raise get_ptb_error(e) from e

    async def _edit_media(
        self,
        chat_id: int,
        message_id: int,
        media,
        mapping: CallbackDataMapping,
        caption: str | None,
        parse_mode: str | None,
        button_rows: ButtonRows | None,
        edit_media_method,  # callable
    ) -> int:
        try:
            reply_markup = self._prepare_reply_markup(mapping, button_rows)

            results = await asyncio.gather(
                edit_media_method(
                    chat_id=chat_id,
                    message_id=message_id,
                    media=media,
                    reply_markup=reply_markup,
                ),
                self.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=message_id,
                    caption=caption,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                ),
                return_exceptions=True,
            )

            media_error = results[0] if isinstance(results[0], Exception) else None
            caption_error = results[1] if isinstance(results[1], Exception) else None

            if (
                media_error
                and isinstance(media_error, MessageNotModified)
                and caption_error
                and isinstance(caption_error, MessageNotModified)
            ):
                raise MessageNotModified("Both media and caption were not modified")

            if media_error and isinstance(media_error, MessageNotModified):
                media_error = None
            if caption_error and isinstance(caption_error, MessageNotModified):
                caption_error = None

            if media_error:
                raise media_error
            if caption_error:
                raise caption_error

            if results[0] and not isinstance(results[0], Exception):
                return results[0].message_id
            elif results[1] and not isinstance(results[1], Exception):
                return results[1].message_id
            else:
                raise ValueError("No successful result from edit operations")

        except Exception as e:
            if isinstance(e, TgBotScreenException):
                raise
            raise get_ptb_error(e) from e

    async def edit_audio(
        self,
        chat_id: int,
        message_id: int,
        audio: Audio,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        return await self._edit_media(
            chat_id=chat_id,
            message_id=message_id,
            media=self.audio_converter.convert(audio),
            mapping=mapping,
            caption=caption,
            parse_mode=parse_mode,
            button_rows=button_rows,
            edit_media_method=self.bot.edit_message_media,
        )

    async def edit_video(
        self,
        chat_id: int,
        message_id: int,
        video: Video,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        return await self._edit_media(
            chat_id=chat_id,
            message_id=message_id,
            media=self.video_converter.convert(video),
            mapping=mapping,
            caption=caption,
            parse_mode=parse_mode,
            button_rows=button_rows,
            edit_media_method=self.bot.edit_message_media,
        )

    async def edit_document(
        self,
        chat_id: int,
        message_id: int,
        document: Document,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        return await self._edit_media(
            chat_id=chat_id,
            message_id=message_id,
            media=self.document_converter.convert(document),
            mapping=mapping,
            caption=caption,
            parse_mode=parse_mode,
            button_rows=button_rows,
            edit_media_method=self.bot.edit_message_media,
        )

    async def edit_photo(
        self,
        chat_id: int,
        message_id: int,
        photo: Photo,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        return await self._edit_media(
            chat_id=chat_id,
            message_id=message_id,
            media=self.photo_converter.convert(photo),
            mapping=mapping,
            caption=caption,
            parse_mode=parse_mode,
            button_rows=button_rows,
            edit_media_method=self.bot.edit_message_media,
        )

    async def edit_voice(
        self,
        chat_id: int,
        message_id: int,
        voice: Voice,
        mapping: CallbackDataMapping,
        caption: str | None = None,
        parse_mode: str | None = None,
        button_rows: ButtonRows | None = None,
    ) -> int:
        return await self._edit_media(
            chat_id=chat_id,
            message_id=message_id,
            media=self.voice_converter.convert(voice),
            mapping=mapping,
            caption=caption,
            parse_mode=parse_mode,
            button_rows=button_rows,
            edit_media_method=self.bot.edit_message_media,
        )
