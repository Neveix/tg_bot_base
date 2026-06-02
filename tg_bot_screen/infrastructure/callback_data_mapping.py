from ..core.models.callback_data import CallbackData
from ..core.interfaces import CallbackDataMapping

class CallbackDataMappingImpl(CallbackDataMapping):
    def __init__(self):
        self.items: list[tuple[CallbackData, str]] = []
    
    def add(self, callback: CallbackData, uuid: str):
        self.items.append((callback, uuid))
    
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