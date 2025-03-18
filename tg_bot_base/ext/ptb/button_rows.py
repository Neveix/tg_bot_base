from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ...button_rows import ButtonRows as BaseButtonRows
from ...button_rows import PreparedButton as BasePreparedButton
from ...button_rows import Button as BaseButton
from ...button_rows import ButtonRow as BaseButtonRow


class ButtonRows(BaseButtonRows):
    def to_reply_markup(self) -> InlineKeyboardMarkup:
        if not self.is_prepared:
            raise ValueError("ButtonRows is not prepared")
        result = []
        for row in self.rows:
            row_list = []
            for button in row.buttons:
                if not isinstance(button, PreparedButton):
                    raise ValueError(f"{button=} is not prepared")
                row_list.append(button.to_inline_button())
            result.append(row_list)
        return InlineKeyboardMarkup(result)
    
    def clone(self) -> "ButtonRows":
        return ButtonRows(*[row.clone() for row in self.rows])

class PreparedButton(BasePreparedButton):
    def to_inline_button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(self.text
            , callback_data = self.callback_data)
    
    def clone(self) -> "PreparedButton":
        return PreparedButton(self.text, self.callback_data)

class Button(BaseButton):
    def prepare(self) -> "PreparedButton":
        print("called prepare from ext!!!")
        return PreparedButton(self.text, str(uuid4()))
    
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())
        

class ButtonRow(BaseButtonRow): ...