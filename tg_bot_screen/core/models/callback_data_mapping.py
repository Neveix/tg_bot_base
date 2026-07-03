from uuid import uuid4
from tg_bot_screen.core.models.callback_data import CallbackData


class CallbackDataMapping:
    def __init__(self):
        self.items: list[tuple[CallbackData, str]] = []

    def add(self, callback: CallbackData):
        self.items.append(
            (
                callback,
                str(uuid4()),
            )
        )

    def get_by_callback(self, callback: CallbackData):
        for i_callback, uuid in self.items:
            if callback is i_callback:
                return uuid
        raise KeyError(callback)

    def get_by_uuid(self, uuid: str):
        for callback, i_uuid in self.items:
            if uuid == i_uuid:
                return callback
        return None
