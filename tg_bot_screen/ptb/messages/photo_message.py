import pathlib
from typing import Self
from telegram import Bot, InputFile, InputMediaPhoto, Message as PTBMessage
import telegram
from tg_bot_base import ButtonRows

from ...callback_data import CallbackDataMapping
from ...message import PhotoMessage     as BasePhotoMessage
from ...message import SentPhotoMessage     as BaseSentPhotoMessage
from .message import HasButtonRows, Message, SentMessage

class PhotoMessage(BasePhotoMessage, HasButtonRows, Message):
    def __init__(self, photo: bytes | InputFile | pathlib.Path | telegram.PhotoSize, 
            caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        super().__init__(caption, button_rows, parse_mode)
        self.photo = photo
        
    async def send(self, user_id: int, bot: Bot, mapping: CallbackDataMapping):
        ptb_message = await bot.send_photo(user_id, self.photo
            , self.caption, reply_markup=self.get_reply_markup(mapping)
            , parse_mode=self.parse_mode)
        return SentPhotoMessage(self.photo, self.caption,
            ptb_message, self.button_rows, self.parse_mode)
    
    def __eq__(self, other: Self):
        return self.caption == other.caption and \
            self.photo == other.photo and \
            self.button_rows == other.button_rows and \
            self.parse_mode == other.parse_mode
    
    def clone(self) -> Self: 
        return PhotoMessage(self.photo, self.caption, self.button_rows, 
            self.parse_mode)


class SentPhotoMessage(BaseSentPhotoMessage, HasButtonRows, SentMessage):
    def __init__(self, photo: bytes | InputFile | pathlib.Path | telegram.PhotoSize, 
            caption: str, ptb_message: PTBMessage, button_rows: ButtonRows = None, 
            parse_mode: str = None,
            ):
        super().__init__(caption, button_rows, parse_mode)
        self.photo = photo
        self.ptb_message = ptb_message
    
    def change(self, message: PhotoMessage):
        self.caption = message.caption
        self.photo = message.photo
        self.parse_mode = message.parse_mode
        self.button_rows = message.button_rows
    
    async def edit(self, bot: Bot, mapping: CallbackDataMapping):
        orig = self.ptb_message
        reply_markup = self.get_reply_markup(mapping)
        if orig.caption == self.caption and orig.reply_markup == reply_markup \
                and orig.photo[-1] == self.photo:
            return
        self.ptb_message = await bot.edit_message_media(
            media=InputMediaPhoto(self.photo, self.caption, self.parse_mode),
            chat_id=self.ptb_message.chat_id,
            message_id=self.ptb_message.message_id,
            reply_markup = reply_markup)
    
    def __eq__(self, other: Self):
        return self.caption == other.caption and \
            self.photo == other.photo and \
            self.button_rows == other.button_rows and \
            self.parse_mode == other.parse_mode
    
    def clone(self):
        return SentPhotoMessage(self.photo, self.caption, self.ptb_message, self.button_rows,
            self.parse_mode)

    def get_unsent(self):
        return PhotoMessage(
              self.photo
            , self.caption
            , self.button_rows
            , self.parse_mode)