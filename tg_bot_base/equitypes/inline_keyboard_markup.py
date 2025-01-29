from tg_bot_base.equitypes.inline_keyboard_button import InlineKeyboardButton

class InlineKeyboardMarkup:
    def __init__(self, markup: list[list[InlineKeyboardButton]]):
        self.markup = markup