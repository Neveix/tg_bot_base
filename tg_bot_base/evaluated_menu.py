from telegram import InlineKeyboardMarkup, InputMediaPhoto

class EvaluatedMenu:
    pass

class EvaluatedMenuDefault(EvaluatedMenu):
    def __init__(self, text: str, reply_markup: InlineKeyboardMarkup):
        self.text = text
        self.reply_markup = reply_markup

class EvaluatedMenuPhoto(EvaluatedMenu):
    def __init__(self, photos: list[InputMediaPhoto] | None):
        self.photos = photos
