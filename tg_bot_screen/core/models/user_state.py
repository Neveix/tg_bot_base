from tg_bot_screen.core.models.input_callback import InputCallback

from .directory_stack import DirectoryStack
from .callback_data_mapping import CallbackDataMapping
from .screen import UnSentScreen, SentScreen
from .user_sessions import UserSessions


class UserState:
    def __init__(
        self,
        user_id: int,
    ):
        self.user_id = user_id
        self.callback_mapping: CallbackDataMapping | None = None
        self.directory_stack: DirectoryStack = DirectoryStack()
        self.media_group_id: str | None = None
        self.input_callback: InputCallback | None = None
        self.screen: SentScreen | None = None
        self.screen_buffer: UnSentScreen | None = None
        self.sessions = UserSessions(self.directory_stack)

    def set_input_callback(self, value: InputCallback | None) -> None:
        self.input_callback = value

    def __repr__(self):
        return f"{type(self).__name__}({self.user_id!r})"
