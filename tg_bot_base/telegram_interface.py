from typing import Sequence

from telegram import InputMedia
from .bot_manager import BotManager
from .button_rows import ButtonRows
class TelegramInterface:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager

    async def send_message(self, user_id: int, text: str, 
            button_rows: ButtonRows | None = None, 
            parse_mode: str | None = None):
        return await self.bot_manager.bot.send_message(
            user_id, text = text, 
            reply_markup = button_rows.to_inline_keyboard(
                user_id = user_id,
                bot_manager = self.bot_manager
            ),
            parse_mode=parse_mode
        )

    async def edit_message(self, user_id: int, message_id: int, 
            text: str, 
            button_rows: ButtonRows | None = None, 
            parse_mode: str | None = None):
        return await self.bot_manager.bot.edit_message_text(
            text = text, chat_id = user_id, message_id = message_id,
            reply_markup = button_rows.to_inline_keyboard(
                user_id = user_id,
                bot_manager = self.bot_manager
            ),
            parse_mode = parse_mode
        )

    async def send_media_group(self, user_id: int, 
            media_list: Sequence[InputMedia]):
        return await self.bot_manager.bot.send_media_group(user_id, media_list)

    async def edit_message_media(self, user_id: int, message_id: int, 
            photo: InputMedia):
        return await self.bot_manager.bot.edit_message_media(
            media = photo, 
            chat_id = user_id, 
            message_id = message_id)
    