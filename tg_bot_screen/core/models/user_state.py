from .directory_stack import DirectoryStack
from .input_callback import InputCallback
from ..interfaces import CallbackDataMapping
from .screen import UnSentScreen, SentScreen
from .user_sessions import UserSessions

from ...infrastructure.callback_data_mapping import CallbackDataMappingImpl


class UserState:
    def __init__(self, 
        user_id: int,
    ):
        self.user_id = user_id
        self.callback_mapping: CallbackDataMapping = CallbackDataMappingImpl()
        self.media_group_id: str | None = None
        self.input_callback: InputCallback | None = None
        self.directory_stack = DirectoryStack()
        self.screen: SentScreen | None = None
        self.screen_buffer: UnSentScreen | None = None
        self.sessions = UserSessions(self.directory_stack)
    
    def reset_input_callback(self):
        self.input_callback = None
    
    def __repr__(self):
        return f"{type(self).__name__}({self.user_id!r})"




