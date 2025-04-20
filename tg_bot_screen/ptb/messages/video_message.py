from telegram import Message as PTBMessage

from .message import HasButtonRows, Message, SentMessage
from ...message import VideoMessage     as BaseVideoMessage
from ...message import SentVideoMessage     as BaseSentVideoMessage


class VideoMessage(BaseVideoMessage, HasButtonRows, Message): ...

class SentVideoMessage(BaseSentVideoMessage, HasButtonRows, SentMessage): ...