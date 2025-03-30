from .input_session import InputSession
from .input_callback import InputCallback
from .callback_data import CallbackData, CallbackDataMapping
from .screen import ReadyScreen, SentScreen

class UserData:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.callback_mapping = CallbackDataMapping()
        self.media_group_id: str = None
        self.input_callback: InputCallback = None
        self.directory_stack: list[str] = []
        self.screen: SentScreen = None
        self.screen_buffer: ReadyScreen = None
        self.__input_session: InputSession = None
    
    @property
    def input_session(self):
        return self.__input_session
    
    @input_session.setter
    def input_session(self, value: InputSession):
        self.__input_session = value
        if value and not value.manual_delete:
            value.directory_level = len(self.directory_stack)
    
    def update_input_session(self):
        new_dir_level = len(self.directory_stack)
        ses = self.__input_session
        if ses and not ses.manual_delete and ses.directory_level > new_dir_level:
            self.__input_session = None

class UserDataManager:
    def __init__(self):
        self.__users_data: dict[int, UserData] = {}
        self.users_data = self.__users_data
    
    def get(self, user_id: int) -> UserData:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = UserData(user_id)
            self.set(user_id, user_data)
        return user_data
    
    def reset(self, user_id: int) -> None:
        self.set(user_id, UserData(user_id))
    
    def set(self, user_id: int, user_data: UserData):
        self.__users_data[user_id] = user_data
