from telegram import Message as PTBMessage

from ...button_rows import Self
from ...core.models.message import VideoNoteMessage as BaseVideoNoteMessage
from ...core.models.message import SentVideoNoteMessage as BaseSentVideoNoteMessage
from .message import Message, SentMessage

class VideoNoteMessage(BaseVideoNoteMessage, Message):
    async def send(self, user_id: int) -> "SentVideoNoteMessage":
        ...
    
    def __eq__(self, other: object) -> bool: 
        if not isinstance(other, VideoNoteMessage):
            return False
        
        return self.text == other.text and \
            self.button_rows == other.button_rows
    
    def clone(self) -> Self: 
        return VideoNoteMessage(self.text, self.button_rows)

class SentVideoNoteMessage(BaseSentVideoNoteMessage, SentMessage): ...