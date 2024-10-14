from telegram import Bot, InlineKeyboardMarkup, InputMediaPhoto

class EvaluatedMenu:
    def __init__(self, text: str = None, reply_markup: InlineKeyboardMarkup = None, photos: list[InputMediaPhoto] = None):
        self.text = text
        self.reply_markup = reply_markup
        self.photos = photos
    def clone(self) -> "EvaluatedMenu":
        if isinstance(self, EvaluatedMenuDefault):
            return EvaluatedMenuDefault.clone(self)
        else:
            return EvaluatedMenuPhoto.clone(self)
    def send(self, bot: Bot, chat_id: int):
        if isinstance(self, EvaluatedMenuDefault):
            EvaluatedMenuDefault.send(self, bot, chat_id)
        else:
            EvaluatedMenuPhoto.send(self, bot, chat_id)


class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup):
        super().__init__(text = text,reply_markup = reply_markup)
    def clone(self) -> "EvaluatedMenuDefault":
        return EvaluatedMenuDefault(self.text, self.reply_markup)
    def send(self, bot: Bot, chat_id: int):
        bot.send_message(chat_id, text = self.text, reply_markup = self.reply_markup)
class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photos: list[InputMediaPhoto]):
        super().__init__(photos=photos)
    def clone(self) -> "EvaluatedMenuPhoto":
        return EvaluatedMenuPhoto(self.photos)
    def send(self, bot: Bot, chat_id: int):
        bot.send_media_group(chat_id, self.photos)