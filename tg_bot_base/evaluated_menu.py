from typing import Any
from telegram import Bot, InputMediaPhoto, Message
from .button_rows import ButtonRows
from .bot_manager import BotManager

class EvaluatedMenuHasNotSendedMessage(Exception):
    pass

class EvaluatedMenu:
    def __init__(self, text: str = None, button_rows: ButtonRows = None, 
            photo: InputMediaPhoto = None):
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
            raise TypeError(f"{self} was wrong type {type(self)}, \
use EvaluatedMenuDefault or EvaluatedMenuPhoto instead")
        result.sended_message = self.sended_message
        return result
    async def send(self, bot_manager: BotManager, chat_id: int):
        if isinstance(self, EvaluatedMenuPhoto):
            await EvaluatedMenuPhoto.send(self, bot_manager, chat_id)
        else:
            await EvaluatedMenuDefault.send(self, bot_manager, chat_id)
    async def edit_message(self, bot_manager: BotManager, chat_id: int, message_id: int):
        if isinstance(self, EvaluatedMenuPhoto):
            await EvaluatedMenuPhoto.edit_message(self, bot_manager, chat_id, message_id)
        else:
            await EvaluatedMenuDefault.edit_message(self, bot_manager, chat_id, message_id)
    def __eq__(self, other: "EvaluatedMenu"):
        list_of_photos = [self.photo, other.photo]
        photos_are_none = all(map(lambda photo: photo is None, list_of_photos))
        photos_are_photos = all(map(lambda photo: isinstance(photo, InputMediaPhoto), list_of_photos))
        photos_are_equal_photos = False
        if photos_are_photos:
            photos_are_equal_photos = self.photo.media == other.photo.media
        photos_are_equal = photos_are_equal_photos or photos_are_none
        result = self.text is other.text and \
            self.button_rows == other.button_rows and \
            photos_are_equal
        return result

class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, button_rows: ButtonRows):
        if text is None:
            raise ValueError("text is None")
        if button_rows is None:
            raise ValueError("button_rows is None")
        super().__init__(text = text, button_rows = button_rows)
    async def send(self, bot_manager: BotManager, chat_id: int):
        bot: Bot = bot_manager.bot
        self.sended_message = await bot.send_message(chat_id, 
            text = self.text, 
            reply_markup = self.button_rows.to_inline_keyboard(
                user_id = chat_id,
                bot_manager = bot_manager
            )
        )
    async def edit_message(self, bot_manager: BotManager, chat_id: int, message_id: int):
        bot = bot_manager.bot
        self.sended_message = await bot.edit_message_text(
            text = self.text, chat_id = chat_id, message_id = message_id,
            reply_markup = self.button_rows.to_inline_keyboard(
                user_id = chat_id,
                bot_manager = bot_manager
            )
        )
    def __repr__(self) -> str:
        return f"""EvaluatedMenuDefault (text = {self.text})"""
    def to_dict(self) -> dict[str, Any]:
        return {
            "text" : self.text,
            "button_rows" : self.button_rows
        }
        
class PhotoIsNone(Exception):
    pass
class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photo: InputMediaPhoto):
        if photo is None:
            raise PhotoIsNone()
        super().__init__(photo=photo)
    async def send(self, bot_manager: BotManager, chat_id: int):
        bot: Bot = bot_manager.bot
        self.sended_message = (await bot.send_media_group(chat_id, [self.photo]))[0]
    async def edit_message(self, bot_manager: BotManager, chat_id: int, message_id: int):
        bot = bot_manager.bot
        self.sended_message = await bot.edit_message_media(media = self.photo, chat_id = chat_id, message_id = message_id)
    def __repr__(self) -> str:
        return f"""EvaluatedMenuPhoto (photo = {self.photo})"""
    def to_dict(self) -> dict[str, InputMediaPhoto]:
        return {
            "photo" : self.photo
        }