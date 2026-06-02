from abc import ABC, abstractmethod
from .models.callback_data import CallbackData
from .models.user_state import UserState


class CallbackDataMapping(ABC):
    @abstractmethod
    def add(self, callback: CallbackData, uuid: str) -> None:
        ...
    
    @abstractmethod
    def get_by_callback(self, callback: CallbackData) -> str:
        ...
    
    @abstractmethod
    def get_by_uuid(self, uuid: str) -> CallbackData | None:
        ...
        


class UserStateStore(ABC):
    @abstractmethod
    def get(self, user_id: int) -> UserState:
        ...
    
    @abstractmethod
    def reset(self, user_id: int) -> None:
        ...
    
    @abstractmethod
    def set(self, user_id: int, user_data: UserState) -> None:
        ...