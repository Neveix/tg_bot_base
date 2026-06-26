from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ...core.models.button_rows import ButtonRows
from ...core.interfaces import ButtonRowsToReplyMarkupConverter, CallbackDataMapping


class ButtonRowsToReplyMarkupConverterPtb(ButtonRowsToReplyMarkupConverter):
    def convert(
        self,
        mapping: CallbackDataMapping,
        button_rows: ButtonRows | None = None,
    ):
        if button_rows is None:
            return InlineKeyboardMarkup([])

        result = []
        for row in button_rows.rows:
            row_l = []
            result.append(row_l)
            for button in row.buttons:
                if button.callback_data is not None:
                    callback_data_str = mapping.get_by_callback(button.callback_data)
                    row_l.append(
                        InlineKeyboardButton(
                            text=button.text,
                            callback_data=callback_data_str,
                        )
                    )
                    continue

                if button.url is not None:
                    row_l.append(
                        InlineKeyboardButton(
                            text=button.text,
                            url=button.url,
                        )
                    )

                if button.web_app is not None:
                    row_l.append(
                        InlineKeyboardButton(
                            text=button.text,
                            url=button.url,
                        )
                    )
        return InlineKeyboardMarkup(result)
