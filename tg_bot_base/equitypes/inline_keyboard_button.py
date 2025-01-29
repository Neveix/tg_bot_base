

class InlineKeyboardButton:
    def __init__(self, text: str, callback_data: str, url: str = None):
        self.text = text
        self.callback_data = callback_data
        if url:
            self.url = url
