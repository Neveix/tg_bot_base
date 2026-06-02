from abc import abstractmethod, ABC
from typing import Callable, Self
from .core.models.screen import DynamicScreen
from .core.models.callback_data import CallbackData
from .core.models.user_state import UserDataManager
from .core.models.user_screen import UserScreen

class BotManager(ABC):
    def __init__(self):
        self.system_user_data: UserDataManager
        self.screen: UserScreen
    
    @abstractmethod
    def build(self) -> Self: 
        # user_datam = UserDataManager()
        # screen = UserScreen(user_datam)
        # self.system_user_data = user_datam
        # self.screen = screen
        # return self
        ...
    
    @abstractmethod
    def add_handlers(self): ...
    

    def dynamic_screen(self, name: str | None = None):
        def decorator(func: Callable):
            nonlocal name
            if name is None:
                name = func.__name__
            self.screen.append_screen(DynamicScreen(name, func))
        return decorator


    
    
