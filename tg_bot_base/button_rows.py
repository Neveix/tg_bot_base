from abc import abstractmethod
from uuid import uuid4
from .callback_data import CallbackData

class Button:
    def __init__(self, text: str, callback_data: CallbackData):
        if not isinstance(text, str) or len(text) < 1:
            raise ValueError(f"{text=} is not str or its length is wrong")
        if not isinstance(callback_data, CallbackData):
            raise ValueError(f"{callback_data=} is not CallbackData")
        self.text = text
        self.callback_data = callback_data
    
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())

    def __eq__(self, other: "Button"):
        return (self.text == other.text and \
            self.callback_data == other.callback_data)
        
    def prepare(self) -> "PreparedButton":
        return PreparedButton(self.text, str(uuid4()))
    
class PreparedButton(Button):
    def __init__(self, text: str, callback_data: str):
        if not isinstance(text, str):
            raise ValueError(f"{text=} expected str")
        if not isinstance(callback_data, str):
            raise ValueError(f"{callback_data=} expected str")
        self.text = text
        self.callback_data = callback_data
    
    def clone(self) -> "PreparedButton":
        return PreparedButton(self.text, self.callback_data)

class ButtonRow:
    def __init__(self, *buttons: Button):
        self.buttons: list[Button] = []
        self.extend(buttons)
    
    def extend(self, buttons: list[Button]):
        self.buttons.extend(buttons)
        return self

    def append(self, button: Button):
        self.buttons.append(button)
        return self
    
    def clone(self) -> "ButtonRow":
        return ButtonRow().\
            extend(
                [button.clone() for button in self.buttons]
            )
    def __eq__(self, other: "ButtonRow"):
        return all([
            button1 == button2 
            for button1, button2
            in zip(self.buttons, other.buttons)])

class ButtonRows:
    def __init__(self, *rows: ButtonRow):
        self.rows: list[ButtonRow] = []
        self.extend(rows)
        self.is_prepared = False
    
    def extend(self, rows: list[ButtonRow]):
        self.rows.extend(rows)
    
    def append(self, row: ButtonRow):
        self.rows.append(row)
    
    def clone(self) -> "ButtonRows":
        return ButtonRows(*[row.clone() for row in self.rows])
    
    def __eq__(self, other: "ButtonRows"):
        return all([row1 == row2
            for row1, row2 in zip(self.rows,other.rows)])
    
    @abstractmethod
    def to_reply_markup(self): ...
    
    def prepare(self) -> dict[str, CallbackData]:
        self.is_prepared = True
        callback_data = {}
        for row in self.rows:
            new_buttons = []
            for button in row.buttons:
                prepared = button.prepare()
                callback_data[prepared.callback_data] = button.callback_data
                new_buttons.append(prepared)
            row.buttons = new_buttons
        return callback_data