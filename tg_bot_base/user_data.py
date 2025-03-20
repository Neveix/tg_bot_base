from .func_data import FuncData
from .callback_data import CallbackData, CallbackDataMapping
from .screen import SentScreen

class UserData:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.callback_mapping = CallbackDataMapping()
        self.media_group_id: str = None
        self.after_input: FuncData = None
        self.directory_stack: list[str] = []
        self.screen: SentScreen = None

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
