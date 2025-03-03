from typing import Sequence, TYPE_CHECKING
from abc import ABC, abstractmethod
from telegram import InputMedia
from .button_rows import ButtonRows
if TYPE_CHECKING:
    from .bot_manager import BotManager

class TgInterface(ABC):
    def __init__(self, bot_manager: "BotManager"):
        self.bot_manager = bot_manager

    @abstractmethod
    async def send_audio(**kwargs): ...

    @abstractmethod
    async def send_document(**kwargs): ...

    @abstractmethod
    async def send_media_group(**kwargs): ...

    @abstractmethod
    async def send_message(**kwargs): ...

    @abstractmethod
    async def send_photo(**kwargs): ...

    @abstractmethod
    async def send_video(**kwargs): ...


