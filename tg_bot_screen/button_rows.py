from abc import abstractmethod
from uuid import uuid4
from .callback_data import CallbackData

def check(obj, condition: bool):
    if not condition:
        raise ValueError(f"{obj=} is wrong")

class Button:
    def __init__(self, text: str, callback_data: CallbackData, url: str = None):
        assert isinstance(text, str),  len(text) > 0 
        assert isinstance(callback_data, CallbackData) 
        assert not url or isinstance(url, str) 
        
        self.text = text
        self.callback_data = callback_data
        self.url = url
    
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())

    def __eq__(self, other: "Button"):
        return (self.text == other.text and \
            self.callback_data == other.callback_data)

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
    
    def get_callback_data(self):
        result: list[CallbackData] = []
        for row in self.rows:
            for button in row.buttons:
                result.append(button.callback_data)
        return result