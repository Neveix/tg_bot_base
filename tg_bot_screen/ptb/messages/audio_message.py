import pathlib
from typing import Self
from telegram import Bot, InputFile, InputMediaAudio
import telegram
from telegram import Message as PTBMessage

from ..button_rows import ButtonRows

from ...callback_data import CallbackDataMapping
from ...message import AudioMessage     as BaseAudioMessage
from ...message import SentAudioMessage     as BaseSentAudioMessage
from .message import HasButtonRows, Message, SentMessage


# TODO: Доработать классы, сейчас они вообще не готовы

class AudioMessage(BaseAudioMessage, HasButtonRows, Message):
    def __init__(self, 
            audio: InputFile | bytes | pathlib.Path | telegram.Audio, 
            caption: str, 
            button_rows: ButtonRows = None, *, 
            parse_mode: str | None = None,
            filename: str = None
        ):
        super().__init__(caption, button_rows, parse_mode)
        self.audio = audio
        self.filename = filename
    
    async def send(self, user_id: int, bot: Bot, mapping: CallbackDataMapping):
        ptb_message = await bot.send_audio(user_id, self.audio, 
            caption = self.caption, 
            reply_markup=self.get_reply_markup(mapping), 
            parse_mode = self.parse_mode)
        return SentAudioMessage(self.audio, ptb_message,
            caption = self.caption, 
            button_rows = self.button_rows, 
            parse_mode = ptb_message, 
            filename = self.filename)
    
    def __eq__(self, other: Self):
        return self.caption == other.caption and \
            self.audio == other.audio and \
            self.button_rows == other.button_rows and \
            self.parse_mode == other.parse_mode
    
    def clone(self):
        button_rows = None
        if self.button_rows:
            button_rows = self.button_rows.clone()
        return AudioMessage(self.audio, self.caption, button_rows, 
            parse_mode=self.parse_mode, filename = self.filename)
        
    def transform(self, old: "SentMessage"):
        return SentAudioMessage(self.audio, old.ptb_message, 
            caption = self.caption, 
            button_rows = self.button_rows, 
            parse_mode = self.parse_mode, 
            filename = self.filename)

class SentAudioMessage(BaseSentAudioMessage, HasButtonRows, SentMessage):
    def __init__(self, 
            audio: bytes | InputFile | pathlib.Path | telegram.Audio,
            ptb_message: PTBMessage | None,
            caption: str | None = None, 
            button_rows: ButtonRows | None = None, *,
            parse_mode: str | None = None,
            filename: str | None = None
        ):
        super().__init__(caption, button_rows, parse_mode)
        self.audio = audio
        self.ptb_message = ptb_message 
        self.__ptb_message_audio = audio
        self.filename = filename
    
    async def edit(self, bot: Bot, mapping: CallbackDataMapping):
        orig = self.ptb_message
        reply_markup = self.get_reply_markup(mapping)
        if  orig.caption_html == self.caption \
                and orig.reply_markup == reply_markup \
                and self.__ptb_message_audio == self.audio \
                and (
                    not isinstance(self.__ptb_message_audio, telegram.Audio)
                    or self.__ptb_message_audio.file_name == self.filename
                ):
            return
        self.ptb_message = await bot.edit_message_media(
            media=InputMediaAudio(self.audio, self.caption, 
                parse_mode=self.parse_mode, filename=self.filename),
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id,
            reply_markup = reply_markup)
        self.__ptb_message_audio = self.audio
    
    def __eq__(self, other: Self):
        return self.caption == other.caption and \
            self.audio == other.audio and \
            self.button_rows == other.button_rows and \
            self.parse_mode == other.parse_mode and \
            self.filename == other.filename
    
    def clone(self):
        return self.__class__(self.audio, self.ptb_message, 
            caption = self.caption, 
            button_rows = self.button_rows,
            parse_mode = self.parse_mode, 
            filename = self.filename)
    
    def get_unsent(self):
        return AudioMessage(
            self.audio, 
            caption = self.caption, 
            button_rows = self.button_rows, 
            parse_mode = self.parse_mode, 
            filename=self.filename)