from ..interfaces import CallbackDataMapping, InputCallback, DirectoryStack
from .screen import UnSentScreen, SentScreen
from .user_sessions import UserSessions


class UserState:
    def __init__(self, 
        user_id: int,
        callback_mapping: CallbackDataMapping,
        directory_stack: DirectoryStack,
    ):
        self.user_id = user_id
        self.callback_mapping = callback_mapping
        self.directory_stack = directory_stack
        self.media_group_id: str | None = None
        self.input_callback: InputCallback | None = None
        self.screen: SentScreen | None = None
        self.screen_buffer: UnSentScreen | None = None
        self.sessions = UserSessions(self.directory_stack)
    
    def reset_input_callback(self):
        self.input_callback = None
    
    def __repr__(self):
        return f"{type(self).__name__}({self.user_id!r})"




