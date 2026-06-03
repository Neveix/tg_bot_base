from abc import ABC, abstractmethod
from typing import Self
from .models.user_state import UserState
from .models.callback_data_use_params import CallbackDataUseParams


class CallbackData(ABC):
    @abstractmethod
    def clone(self) -> Self: ...
    
    @abstractmethod
    async def use(self, *, params: CallbackDataUseParams, **kwargs): ...


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