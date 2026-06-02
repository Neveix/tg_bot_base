from abc import ABC, abstractmethod
from telegram import Bot, Message as PTBMessage
import telegram

from ..button_rows import ButtonRows
from ...core.models.callback_data import CallbackDataMapping
from ...core.models.message import UnSentMessage as BaseMessage
from ...core.models.message import SentMessage as BaseSentMessage
from ...core.models.message import HasButtonRows as BaseHasButtonRows

class HasButtonRows(BaseHasButtonRows):
    def __init__(self):
        self.button_rows: ButtonRows | None = None
        
    def get_reply_markup(self, mapping: CallbackDataMapping):
        if self.button_rows:
            rm = self.button_rows.to_reply_markup(mapping)
            if len(rm.inline_keyboard) == 0:
                return None
            return rm
        return None


class Message(BaseMessage, ABC):
    @abstractmethod
    def transform(self, old: "SentMessage") -> "SentMessage":
        ...
    

class SentMessage(BaseSentMessage):
    def __init__(self):
        self.ptb_message: PTBMessage = None
    
    async def delete(self, bot: Bot):
        try:
            await bot.delete_message(
                chat_id=self.ptb_message.chat_id,
                message_id=self.ptb_message.message_id)
        except telegram.error.BadRequest as e:
            print(f"{self} не получилось удалить: {e!r}")
    
    @abstractmethod
    async def edit(self, bot: Bot, mapping: CallbackDataMapping): ...