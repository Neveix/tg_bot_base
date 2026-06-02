from ..core.models.user_state import UserState
from ..core.interfaces import UserStateStore




class UserStateStoreImpl(UserStateStore):
    def __init__(self):
        self.__users_data: dict[int, UserState] = {}
    
    def get(self, user_id: int) -> UserState:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = UserState(user_id)
            self.set(user_id, user_data)
        return user_data
    
    def reset(self, user_id: int) -> None:
        self.set(user_id, UserState(user_id))
    
    def set(self, user_id: int, user_data: UserState):
        self.__users_data[user_id] = user_data
