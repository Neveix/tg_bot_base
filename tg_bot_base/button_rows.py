from multiprocessing import Value
from .callback_data import CallbackData

class Button:
    def __init__(self, text: str, callback_data: CallbackData):
        if not isinstance(text, str) or len(text) < 1:
            raise ValueError("Variable text is not of type str or its length less than 1")
        if not isinstance(callback_data, CallbackData):
            raise ValueError("Variable callback_data is not of type CallbackData")
        self.text = text
        self.callback_data = callback_data
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())

class ButtonRow:
    def __init__(self, *buttons: Button):
        self.buttons: list[Button] = []
        self.extend(buttons)
    def extend(self, *buttons: Button) -> "ButtonRow":
        for button in buttons:
            if not isinstance(button, Button):
                raise ValueError("button is not of type Button")
            self.buttons.append(button)
        return self
    def clone(self) -> "ButtonRow":
        return ButtonRow().\
            extend(
                [button.clone() for button in self.buttons]
            )

class ButtonRows:
    def __init__(self, *rows: ButtonRow):
        self.rows: list[ButtonRow] = []
        self.extend(rows)
    def extend(self, *rows: ButtonRow) -> "ButtonRow":
        for row in rows:
            if not isinstance(row, ButtonRow):
                raise ValueError("row is not of type ButtonRow")
            self.rows.append(row)
        return self
    def clone(self) -> "ButtonRows":
        return ButtonRows().\
            extend(
                [row.clone() for row in self.rows]
            )
