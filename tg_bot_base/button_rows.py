from .callback_data import CallbackData

class Button:
    def __init__(self, text: str, callback_data: CallbackData):
        if not isinstance(text, str) or len(text) < 1:
            raise ValueError("Variable text is not of type str or its length less than 1")
        if not isinstance(callback_data, CallbackData):
            raise ValueError("Variable callback_data is not of type CallbackData")
        self.text = text
        self.callback_data = callback_data

class ButtonRow:
    def __init__(self):
        self.buttons: list[Button] = []
    def append(self, button: Button) -> None:
        self.buttons.append(button)

class ButtonRows:
    def __init__(self):
        self.rows: list[ButtonRow] = []
    def append(self, row: ButtonRow) -> None:
        self.rows.append(row)
