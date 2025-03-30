from telegram import Message as PTBMessage

from .message import HasButtonRows, Message, SentMessage
from ...message import DocumentMessage  as BaseDocumentMessage
from ...message import SentDocumentMessage  as BaseSentDocumentMessage


class DocumentMessage(BaseDocumentMessage, Message): ...

class SentDocumentMessage(BaseSentDocumentMessage, HasButtonRows, SentMessage): ...