from dataclasses import dataclass, field
from typing import Any
from .callback_data_impl import CallbackData

@dataclass(frozen=True)
class Button:
    text: str
    callback_data: CallbackData
    url: str | None = None
    web_app: Any | None = None

@dataclass(frozen=True)
class ButtonRow:
    buttons: list[Button] = field(default_factory=list)

@dataclass(frozen=True)
class ButtonRows:
    rows: list[ButtonRow] = field(default_factory=list)
    
    def get_callback_data(self) -> list[CallbackData]:
        result = []
        for row in self.rows:
            for button in row.buttons:
                result.append(button.callback_data)
        return result

