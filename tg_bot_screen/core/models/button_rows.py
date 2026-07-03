from dataclasses import dataclass
from typing import Any

from tg_bot_screen.core.models.callback_data import CallbackData


@dataclass(frozen=True)
class Button:
    text: str
    callback_data: CallbackData | None = None
    url: str | None = None
    web_app: Any | None = None


class ButtonRow:
    def __init__(self, *buttons: Button):
        self.buttons: list[Button] = list(buttons)


class ButtonRows:
    def __init__(self, *rows: ButtonRow):
        self.rows: list[ButtonRow] = list(rows)

    def get_callback_data(self) -> list[CallbackData]:
        result = []
        for row in self.rows:
            for button in row.buttons:
                result.append(button.callback_data)
        return result
