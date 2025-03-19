from abc import ABC
import pathlib
from typing import Any, Self

from telegram import Bot, InputFile
from telegram import Message as PTBMessage
import telegram
from ...button_rows import ButtonRows
from ...message import Message          as BaseMessage
from ...message import AudioMessage     as BaseAudioMessage
from ...message import VideoMessage     as BaseVideoMessage
from ...message import DocumentMessage  as BaseDocumentMessage
from ...message import SimpleMessage    as BaseSimpleMessage
from ...message import VideoNoteMessage as BaseVideoNoteMessage
from ...message import PhotoMessage     as BasePhotoMessage

from ...message import Message              as BaseSentMessage
from ...message import SentAudioMessage     as BaseSentAudioMessage
from ...message import SentVideoMessage     as BaseSentVideoMessage
from ...message import SentDocumentMessage  as BaseSentDocumentMessage
from ...message import SentSimpleMessage    as BaseSentSimpleMessage
from ...message import SentVideoNoteMessage as BaseSentVideoNoteMessage
from ...message import SentPhotoMessage     as BaseSentPhotoMessage

class HasButtonRows(ABC):
    def get_reply_markup(self):
        if self.button_rows:
            return self.button_rows.to_reply_markup()
        return None

class AudioMessage(BaseAudioMessage, HasButtonRows):
    def __init__(self
        , audio: str | InputFile | bytes | pathlib.Path | telegram.Audio
        , caption: str, button_rows: ButtonRows):
        super().__init__(audio, caption, button_rows)
        self.audio = audio

class DocumentMessage(BaseDocumentMessage): ...

class SimpleMessage(BaseSimpleMessage, HasButtonRows):
    async def send(self, user_id: int, bot: Bot):
        ptb_message = await bot.send_message(user_id, self.text
            , reply_markup=self.get_reply_markup())
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

class SentAudioMessage(BaseSentAudioMessage, HasButtonRows): ...

class SentDocumentMessage(BaseSentDocumentMessage, HasButtonRows): ...

class SentSimpleMessage(BaseSentSimpleMessage, HasButtonRows):
    def __init__(self, text: str, button_rows: ButtonRows
        , ptb_message: PTBMessage):
        super().__init__(text, button_rows)
        self.ptb_message = ptb_message 
    
    def change(self, message: SimpleMessage):
        self.text = message.text
        self.button_rows = message.button_rows
        
    
    async def edit(self, bot: Bot):
        orig = self.ptb_message
        reply_markup = self.get_reply_markup()
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


class SentPhotoMessage(BaseSentPhotoMessage, HasButtonRows): ...

class SentVideoMessage(BaseSentVideoMessage, HasButtonRows): ...

class SentVideoNoteMessage(BaseSentVideoNoteMessage): ...