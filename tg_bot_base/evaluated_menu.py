from typing import Any, TYPE_CHECKING
from abc import ABC, abstractmethod
from telegram import Message
from .button_rows import ButtonRows
if TYPE_CHECKING:
    from .bot_manager import BotManager

class EvaluatedMenuHasNotSendedMessage(Exception):
    pass

class EvaluatedMenu(ABC):
    """base for EvaluatedMenuDefault and EvaluatedMenuPhoto"""
    def __init__(self, text: str = None, button_rows: ButtonRows = None, 
            photo: bytes = None):
        self.text = text
        self.button_rows = button_rows
        self.photo = photo
        self.sended_message: Message = None
    
    def clone(self) -> "EvaluatedMenu":
        if isinstance(self, EvaluatedMenuPhoto):
            result = EvaluatedMenuPhoto(self.photo)
        elif isinstance(self, EvaluatedMenuDefault):
            result = EvaluatedMenuDefault(self.text, self.button_rows)
        else:
            raise TypeError("use EvaluatedMenuDefault or EvaluatedMenuPhoto instead")
        result.sended_message = self.sended_message
        return result
    
    @abstractmethod
    async def send_message(self, bot_manager: "BotManager", user_id: int) -> None:
        pass

    @abstractmethod
    async def edit_message(self, bot_manager: "BotManager", user_id: int, message_id: int) -> None:
        pass

    def __eq__(self, other: "EvaluatedMenu"):
        list_of_photos = [self.photo, other.photo]
        photos_are_none = all(map(lambda photo: photo is None, list_of_photos))
        photos_are_photos = all(map(lambda photo: isinstance(photo, bytes), list_of_photos))
        photos_are_equal_photos = False
        if photos_are_photos:
            photos_are_equal_photos = self.photo.media == other.photo.media
        photos_are_equal = photos_are_equal_photos or photos_are_none
        result = self.text is other.text and \
            self.button_rows == other.button_rows and \
            photos_are_equal
        return result

class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, button_rows: ButtonRows, 
            parse_mode: str | None = None):
        if text is None:
            raise ValueError("text is None")
        if button_rows is None:
            raise ValueError("button_rows is None")
        super().__init__(text = text, button_rows = button_rows)
        self.parse_mode = parse_mode
    
    async def send_message(self, bot_manager: "BotManager", user_id: int) -> None:
        self.sended_message = await bot_manager.tg_interface.send_message(
            user_id = user_id,
            text = self.text,
            button_rows = self.button_rows,
            parse_mode = self.parse_mode)
    
    async def edit_message(self, bot_manager: "BotManager", user_id: int, message_id: int) -> None:
        self.sended_message = await bot_manager.tg_interface.edit_message(
            message_id = message_id,
            user_id = user_id,
            text = self.text,
            button_rows = self.button_rows,
            parse_mode = self.parse_mode)
    
    def __repr__(self) -> str:
        return f"""EvaluatedMenuDefault (text = {self.text})"""
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "text" : self.text,
            "button_rows" : self.button_rows
        }
    
class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photo: bytes):
        if photo is None:
            raise ValueError("photo is None")
        super().__init__(photo=photo)
    async def send_message(self, bot_manager: "BotManager", user_id: int) -> None:
        self.sended_message = (await bot_manager.tg_interface.send_media_group(
            user_id = user_id,
            media_list = [self.photo]
        ))[0]
    async def edit_message(self, bot_manager: "BotManager", user_id: int, message_id: int) -> None:
        self.sended_message = await bot_manager.tg_interface.edit_message_media(
            user_id = user_id,
            message_id = message_id,
            photo = self.photo
        )
    def __repr__(self) -> str:
        return f"""EvaluatedMenuPhoto (photo = {self.photo})"""
    def to_dict(self) -> dict[str, bytes]:
        return {
            "photo" : self.photo
        }