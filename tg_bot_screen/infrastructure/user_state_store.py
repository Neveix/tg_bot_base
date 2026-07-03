from typing import Protocol

from ..core.models.user_state import UserState
from ..core.interfaces import UserStateStore


class UserStateFactory(Protocol):
    def __call__(self, user_id: int) -> UserState: ...


class UserStateStoreImpl(UserStateStore):
    def __init__(
        self,
        user_state_factory: UserStateFactory,
    ):
        self.__users_data: dict[int, UserState] = {}
        self.user_state_factory = user_state_factory

    def get(self, user_id: int) -> UserState:
        user_data = self.__users_data.get(user_id)
        if user_data is None:
            user_data = self.user_state_factory(user_id)
            self.set(user_id, user_data)
        return user_data

    def reset(self, user_id: int) -> None:
        self.set(user_id, self.user_state_factory(user_id))

    def set(self, user_id: int, user_data: UserState):
        self.__users_data[user_id] = user_data
