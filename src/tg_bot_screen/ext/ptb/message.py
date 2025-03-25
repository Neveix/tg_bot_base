from abc import ABC
import pathlib
from typing import Any, Self

from telegram import Bot, InputFile
from telegram import Message as PTBMessage
import telegram

from ...callback_data import CallbackDataMapping
from ...button_rows import ButtonRows
from ...message import Message          as BaseMessage
from ...message import AudioMessage     as BaseAudioMessage
from ...message import VideoMessage     as BaseVideoMessage
from ...message import DocumentMessage  as BaseDocumentMessage
from ...message import SimpleMessage    as BaseSimpleMessage
from ...message import VideoNoteMessage as BaseVideoNoteMessage
from ...message import PhotoMessage     as BasePhotoMessage

from ...message import SentMessage          as BaseSentMessage
from ...message import SentAudioMessage     as BaseSentAudioMessage
from ...message import SentVideoMessage     as BaseSentVideoMessage
from ...message import SentDocumentMessage  as BaseSentDocumentMessage
from ...message import SentSimpleMessage    as BaseSentSimpleMessage
from ...message import SentVideoNoteMessage as BaseSentVideoNoteMessage
from ...message import SentPhotoMessage     as BaseSentPhotoMessage

class HasButtonRows(ABC):
    def get_reply_markup(self, mapping: CallbackDataMapping):
        if self.button_rows:
            return self.button_rows.to_reply_markup(mapping)
        return None

class AudioMessage(BaseAudioMessage, HasButtonRows):
    def __init__(self, 
            audio: InputFile | bytes | pathlib.Path | telegram.Audio, 
            caption: str, button_rows: ButtonRows = None, parse_mode: str = None):
        super().__init__(caption, button_rows, parse_mode)
        self.audio = audio
    
    async def send(self, user_id: int, bot: Bot, mapping: CallbackDataMapping):
        ptb_message = await bot.send_audio(user_id, self.audio
            , caption = self.caption
            , reply_markup=self.get_reply_markup(mapping)\
            , parse_mode = self.parse_mode)
        return SentSimpleMessage( # TODO: fix
            self.text, self.button_rows, ptb_message)
    
    def __eq__(self, other: "AudioMessage"):
        return self.caption == other.caption and \
            self.audio == other.audio and \
            self.button_rows == other.button_rows
    
    def clone(self):
        button_rows = None
        if self.button_rows:
            button_rows = self.button_rows.clone()
        return AudioMessage(self.audio, self.caption, button_rows, 
            self.parse_mode)

class DocumentMessage(BaseDocumentMessage): ...

class SimpleMessage(BaseSimpleMessage, HasButtonRows):
    async def send(self, user_id: int, bot: Bot, mapping: CallbackDataMapping):
        ptb_message = await bot.send_message(user_id, self.text
            , reply_markup=self.get_reply_markup(mapping))
        return SentSimpleMessage(
            self.text, self.button_rows, ptb_message)
    
    def __eq__(self, other: "SimpleMessage"):
        return self.text == other.text and \
            self.button_rows == other.button_rows
    
    def clone(self):
        button_rows = None
        if self.button_rows:
            button_rows = self.button_rows.clone()
        return SimpleMessage(self.text, button_rows)

class PhotoMessage(BasePhotoMessage, HasButtonRows): ...

class VideoMessage(BaseVideoMessage, HasButtonRows): ...

class VideoNoteMessage(BaseVideoNoteMessage): ...

class SentAudioMessage(BaseSentAudioMessage, HasButtonRows):
    def __init__(self, 
            audio: str, 
            button_rows: ButtonRows
        , ptb_message: PTBMessage):
        super().__init__(text, button_rows)
        self.ptb_message = ptb_message 
    
    def change(self, message: SimpleMessage):
        self.text = message.text
        self.button_rows = message.button_rows
    
    async def edit(self, bot: Bot, mapping: CallbackDataMapping):
        orig = self.ptb_message
        reply_markup = self.get_reply_markup(mapping)
        if orig.text == self.text and orig.reply_markup == reply_markup:
            return
        self.ptb_message = await bot.edit_message_text(
            text = self.text,
            reply_markup = reply_markup,
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id)
    
    async def delete(self, bot: Bot):
        await bot.delete_message(
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id)
    
    def __eq__(self, other: Self):
        return self.text == other.text and \
            self.button_rows == other.button_rows
    
    def clone(self):
        return SentSimpleMessage(self.text, self.button_rows, self.ptb_message)

    def get_unsent(self):
        return SimpleMessage(
              self.text
            , self.button_rows)

class SentDocumentMessage(BaseSentDocumentMessage, HasButtonRows): ...

# TODO: Добавить поддержку других типов сообщений

class SentSimpleMessage(BaseSentSimpleMessage, HasButtonRows):
    def __init__(self, text: str, button_rows: ButtonRows
        , ptb_message: PTBMessage):
        super().__init__(text, button_rows)
        self.ptb_message = ptb_message 
    
    def change(self, message: SimpleMessage):
        self.text = message.text
        self.button_rows = message.button_rows
    
    async def edit(self, bot: Bot, mapping: CallbackDataMapping):
        orig = self.ptb_message
        reply_markup = self.get_reply_markup(mapping)
        if orig.text == self.text and orig.reply_markup == reply_markup:
            return
        self.ptb_message = await bot.edit_message_text(
            text = self.text,
            reply_markup = reply_markup,
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id)
    
    async def delete(self, bot: Bot):
        await bot.delete_message(
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id)
    
    def __eq__(self, other: Self):
        return self.text == other.text and \
            self.button_rows == other.button_rows
    
    def clone(self):
        return SentSimpleMessage(self.text, self.button_rows, self.ptb_message)

    def get_unsent(self):
        return SimpleMessage(
              self.text
            , self.button_rows)


class SentPhotoMessage(BaseSentPhotoMessage, HasButtonRows): ...

class SentVideoMessage(BaseSentVideoMessage, HasButtonRows): ...

class SentVideoNoteMessage(BaseSentVideoNoteMessage): ...