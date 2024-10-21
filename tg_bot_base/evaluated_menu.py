from typing import Any
from telegram import Bot, InlineKeyboardMarkup, InputMediaPhoto, Message

class EvaluatedMenuHasNotSendedMessage(Exception):
    pass

class EvaluatedMenu:
    def __init__(self, text: str = None, reply_markup: InlineKeyboardMarkup = None, 
            photo: InputMediaPhoto = None):
        self.text = text
        self.reply_markup = reply_markup
        self.photo = photo
        self.sended_message: Message = None
    def clone(self) -> "EvaluatedMenu":
        result = None
        if isinstance(self, EvaluatedMenuPhoto):
            result = EvaluatedMenuPhoto(self.photo)
        if isinstance(self, EvaluatedMenuDefault):
            result = EvaluatedMenuDefault(self.text, self.reply_markup)
        result.sended_message = self.sended_message
        return result
    async def send(self, bot: Bot, chat_id: int):
        if isinstance(self, EvaluatedMenuPhoto):
            await EvaluatedMenuPhoto.send(self, bot, chat_id)
        else:
            await EvaluatedMenuDefault.send(self, bot, chat_id)
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        if isinstance(self, EvaluatedMenuPhoto):
            await EvaluatedMenuPhoto.edit_message(self, bot, chat_id, message_id)
        else:
            await EvaluatedMenuDefault.edit_message(self, bot, chat_id, message_id)

class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup):
        if text is None:
            raise ValueError("text is None")
        if reply_markup is None:
            raise ValueError("reply_markup is None")
        super().__init__(text = text,reply_markup = reply_markup)
    async def send(self, bot: Bot, chat_id: int):
        self.sended_message = await bot.send_message(chat_id, text = self.text, reply_markup = self.reply_markup)
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        self.sended_message = await bot.edit_message_text(
            text = self.text, chat_id = chat_id, message_id = message_id,
            reply_markup = self.reply_markup)
    def __repr__(self) -> str:
        return f"""EvaluatedMenuDefault (text = {self.text})"""
    def to_dict(self) -> dict[str, Any]:
        return {
            "text" : self.text,
            "reply_markup" : self.reply_markup
        }
        
class PhotoIsNone(Exception):
    pass
class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photo: InputMediaPhoto):
        if photo is None:
            raise PhotoIsNone()
        super().__init__(photo=photo)
    async def send(self, bot: Bot, chat_id: int):
        self.sended_message = await bot.send_media_group(chat_id, [self.photo])
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        self.sended_message = await bot.edit_message_media(media = self.photo, chat_id = chat_id, message_id = message_id)
    def __repr__(self) -> str:
        return f"""EvaluatedMenuPhoto (photo = {self.photo})"""
    def to_dict(self) -> dict[str, InputMediaPhoto]:
        return {
            "photo" : self.photo
        }