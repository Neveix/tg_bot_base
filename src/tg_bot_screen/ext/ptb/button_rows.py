from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ...callback_data import CallbackDataMapping
from ...button_rows import ButtonRows as BaseButtonRows
from ...button_rows import Button as BaseButton
from ...button_rows import ButtonRow as BaseButtonRow


class ButtonRows(BaseButtonRows):
    def to_reply_markup(self, mapping: CallbackDataMapping
            ) -> InlineKeyboardMarkup:
        result = []
        for row in self.rows:
            row_list = []
            for button in row.buttons:
                row_list.append(button.to_inline_button(mapping))
            result.append(row_list)
        return InlineKeyboardMarkup(result)
    
    def clone(self) -> "ButtonRows":
        return ButtonRows(*[row.clone() for row in self.rows])

class Button(BaseButton):
    def to_inline_button(self, mapping: CallbackDataMapping
            ) -> InlineKeyboardButton:
        uuid = mapping.get_by_callback(self.callback_data)
        return InlineKeyboardButton(self.text
            , callback_data = uuid, url = self.url)
    
    def clone(self) -> "Button":
        return Button(self.text, self.callback_data.clone())
        

class ButtonRow(BaseButtonRow): ...