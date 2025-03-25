from abc import abstractmethod, ABC
from typing import Callable

from .screen import DynamicScreen
from .func_data import FuncData
from .callback_data import GoToScreen, RunFunc, StepBack, CallbackData
from .user_data import UserDataManager
from .user_screen import UserScreen
from .message import Message

class BotManager(ABC):
    def __init__(self):
        self.system_user_data: UserDataManager = None
        self.screen: UserScreen = None
        self.config_delete_old_messages = True
        
    def build(self):
        user_data = UserDataManager()
        screen = UserScreen(user_data)
        self.system_user_data = user_data
        self.screen = screen
        return self
    
    def get_system_user_data(self, user_id: int):
        return self.system_user_data.get(user_id)

    @abstractmethod
    def get_message_handler(self): ...

    async def _handle_message(self, user_id: int, **kwargs):
        user_data = self.get_system_user_data(user_id)
        if self.config_delete_old_messages:
            await self.delete_message(**kwargs)
        
        after_input: FuncData = user_data.after_input
        if after_input is None:
            return
        
        await self.screen.clear(user_id, self.config_delete_old_messages)
        
        if user_data.after_input.one_time:
            user_data.after_input = None
        await after_input.function(user_id=user_id
            , **after_input.kwargs, **kwargs)

    @abstractmethod
    def get_callback_query_handler(self): ...
    
    @abstractmethod
    async def delete_message(self, message): ...
    
    async def _handle_callback_query(self, user_id: int, query_data: str):
        mapping = self.get_system_user_data(user_id).callback_mapping
        data: CallbackData = mapping.get_by_uuid(query_data)
        if data is None:
            return
        
        if isinstance(data, GoToScreen):
            await self.screen.set_by_name(user_id, data.screen_name)
        
        elif isinstance(data, StepBack):
            await self.screen.step_back(user_id)
            
        elif isinstance(data, RunFunc):
            await data.function(user_id=user_id, **data.kwargs)
    
    def dynamic_screen(self, name: str):
        def decorator(func: Callable[[int],list[Message]]):
            self.screen.append_screen(DynamicScreen(name, func))
        return decorator


    
    
