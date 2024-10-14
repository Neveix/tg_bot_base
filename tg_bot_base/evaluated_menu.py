from telegram import Bot, InlineKeyboardMarkup, InputMediaPhoto, Message

class EvaluatedMenuHasNotSendedMessage(Exception):
    pass

class EvaluatedMenu:
    def __init__(self, text: str = None, reply_markup: InlineKeyboardMarkup = None, 
            photo: list[InputMediaPhoto] = None):
        self.text = text
        self.reply_markup = reply_markup
        self.photo = photo
        self.sended_message: Message = None
    def clone(self) -> "EvaluatedMenu":
        if isinstance(self, EvaluatedMenuDefault):
            return EvaluatedMenuDefault.clone(self)
        return EvaluatedMenuPhoto.clone(self)
    async def send(self, bot: Bot, chat_id: int):
        if isinstance(self, EvaluatedMenuDefault):
            await EvaluatedMenuDefault.send(self, bot, chat_id)
        else:
            await EvaluatedMenuPhoto.send(self, bot, chat_id)
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        if isinstance(self, EvaluatedMenuDefault):
            await EvaluatedMenuDefault.edit_message(self, bot, chat_id, message_id)
        else:
            await EvaluatedMenuPhoto.edit_message(self, bot, chat_id, message_id)


class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup):
        super().__init__(text = text,reply_markup = reply_markup)
    def clone(self) -> "EvaluatedMenuDefault":
        return EvaluatedMenuDefault(self.text, self.reply_markup)
    async def send(self, bot: Bot, chat_id: int):
        self.sended_message = await bot.send_message(chat_id, text = self.text, reply_markup = self.reply_markup)
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        self.sended_message = await bot.edit_message_text(text = self.text, chat_id = chat_id, message_id = message_id)
        await bot.edit_message_reply_markup(reply_markup = self.reply_markup, chat_id = chat_id, message_id = message_id)
        
class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photo: list[InputMediaPhoto]):
        super().__init__(photo=photo)
    def clone(self) -> "EvaluatedMenuPhoto":
        return EvaluatedMenuPhoto(self.photo)
    async def send(self, bot: Bot, chat_id: int):
        self.sended_message = await bot.send_media_group(chat_id, self.photo)[0]
    async def edit_message(self, bot: Bot, chat_id: int, message_id: int):
        self.sended_message = await bot.edit_message_media(media = self.photo, chat_id = chat_id, message_id = message_id)