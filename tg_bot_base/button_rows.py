from typing import Any, Callable, TYPE_CHECKING
from uuid import uuid4
from .callback_data import CallbackData
if TYPE_CHECKING:
    from .bot_manager import BotManager

class Button:
    def __init__(self, text: str | Callable, callback_data: CallbackData | Callable):
        if (not isinstance(text, str) or len(text) < 1) and not isinstance(text, Callable):
            raise ValueError(f"{text=} is wrong type or str length")
        if not isinstance(callback_data, CallbackData) and not isinstance(text, Callable):
            raise ValueError(f"{callback_data=} is wrong type ")
        self.text = text
        self.callback_data = callback_data
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())
    def to_dict(self, **kwargs) -> dict[str, Any]:
        result = {}
        if isinstance(self.text, str):
            result["text"] = self.text
        else:
            result["text"] = self.text(**kwargs)
        if isinstance(self.text, str):
            result["callback_data"] = self.callback_data
        else:
            result["callback_data"] = self.callback_data(**kwargs)
        return result
    def __eq__(self, other: "Button"):
        return (
            self.text == other.text and \
            self.callback_data == other.callback_data
        )
            

class ButtonRow:
    def __init__(self, *buttons: Button):
        self.buttons: list[Button] = []
        self.extend(*buttons)
    def extend(self, *buttons: Button) -> "ButtonRow":
        self.buttons.extend(buttons)
        return self
    def append(self, button: Button) -> "ButtonRow":
        self.buttons.append(button)
        return self
    def clone(self) -> "ButtonRow":
        return ButtonRow().\
            extend(
                [button.clone() for button in self.buttons]
            )
    def __eq__(self, other: "ButtonRow"):
        return all(
            map(
                lambda button1, button2: button1 == button2,
                 self.buttons
                ,other.buttons
            )
        )

class ButtonRows:
    def __init__(self, *rows: ButtonRow):
        self.rows: list[ButtonRow] = []
        self.extend(*rows)
    def extend(self, *rows: ButtonRow) -> "ButtonRows":
        self.rows.extend(rows)
        return self
    def append(self, row: ButtonRow) -> "ButtonRows":
        self.rows.append(row)
        return self
    def clone(self) -> "ButtonRows":
        return ButtonRows().\
            extend(
                [row.clone() for row in self.rows]
            )
    def __eq__(self, other: "ButtonRows"):
        return all(
            map(
                lambda row1, row2: row1 == row2,
                self.rows,
                other.rows
            )
        )
    # def to_inline_keyboard(self, 
    #         set_callback_data: bool=True, **kwargs) -> InlineKeyboardMarkup:
    #     reply_markup = []
    #     bot_manager: "BotManager" = kwargs.get("bot_manager")
    #     user_id: int = kwargs.get("user_id")
    #     callback_data = {}
    #     for old_line in self.rows:
    #         line = []
    #         for old_button in old_line.buttons:
    #             old_button_dict = old_button.to_dict(**kwargs)
    #             old_callback_data: CallbackData = old_button_dict["callback_data"]
    #             uuid_code = str(uuid4())
    #             callback_data[uuid_code] = old_callback_data
    #             IKBkwargs = {
    #                  "text" : old_button_dict["text"]
    #                 ,"callback_data" : uuid_code
    #             }
    #             if old_callback_data.action == "url":
    #                 IKBkwargs["url"] = old_callback_data.kwargs["url"]
    #             line.append(InlineKeyboardButton(**IKBkwargs))
    #         reply_markup.append(line)
    #     if set_callback_data:
    #         user_data = bot_manager.user_data_manager.get(user_id)
    #         user_data.callback_data = callback_data
    #     return InlineKeyboardMarkup(reply_markup)