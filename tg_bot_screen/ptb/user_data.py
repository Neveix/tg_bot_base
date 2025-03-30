

from ..user_data import UserData as BaseUserData, \
    UserDataManager as BaseUserDataManager
from .screen import SentScreen
from .input_session import InputSession



class UserData(BaseUserData):
    def __init__(self, user_id: int):
        super().__init__(self, user_id)
        self.screen: SentScreen = None
        self.__input_session: InputSession = None
    
    @property
    def input_session(self):
        return self.__input_session
    
    @input_session.setter
    def input_session(self, value: InputSession):
        super().input_session = value
        if value is None:
            print("input session deleted")
        

class UserDataManager(BaseUserDataManager):
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
