import pathlib
from typing import Any

from telegram import Bot, InputFile
import telegram
from ...button_rows import ButtonRows
from ...message import AudioMessage     as BaseAudioMessage
from ...message import VideoMessage     as BaseVideoMessage
from ...message import DocumentMessage  as BaseDocumentMessage
from ...message import SimpleMessage    as BaseSimpleMessage
from ...message import VideoNoteMessage as BaseVideoNoteMessage
from ...message import PhotoMessage     as BasePhotoMessage

from ...message import SentAudioMessage     as BaseSentAudioMessage
from ...message import SentVideoMessage     as BaseSentVideoMessage
from ...message import SentDocumentMessage  as BaseSentDocumentMessage
from ...message import SentSimpleMessage    as BaseSentSimpleMessage
from ...message import SentVideoNoteMessage as BaseSentVideoNoteMessage
from ...message import SentPhotoMessage     as BaseSentPhotoMessage


class AudioMessage(BaseAudioMessage):
    def __init__(self
        , audio: str | InputFile | bytes | pathlib.Path | telegram.Audio
        , caption: str, button_rows: ButtonRows):
        super().__init__(audio, caption, button_rows)
        self.audio = audio

class DocumentMessage(BaseDocumentMessage): ...

class SimpleMessage(BaseSimpleMessage):
    async def send(self, user_id: int, bot: Bot):
        if self.button_rows:
            reply_markup = self.button_rows.to_reply_markup()
        else:
            reply_markup = None
        await bot.send_message(user_id, self.text
            , reply_markup=reply_markup)
    
    def __eq__(self, other: "SimpleMessage"):
        return self.text == other.text and \
            self.button_rows == other.button_rows
    
    def clone(self):
        return SimpleMessage(self.text, self.button_rows.clone())

class PhotoMessage(BasePhotoMessage): ...

class VideoMessage(BaseVideoMessage): ...

class VideoNoteMessage(BaseVideoNoteMessage): ...


class SentAudioMessage(BaseSentAudioMessage): ...

class SentDocumentMessage(BaseSentDocumentMessage): ...

class SentSimpleMessage(BaseSentSimpleMessage): ...

class SentPhotoMessage(BaseSentPhotoMessage): ...

class SentVideoMessage(BaseSentVideoMessage): ...

class SentVideoNoteMessage(BaseSentVideoNoteMessage): ...