from abc import abstractmethod, ABC
from typing import Callable

from .screen import DynamicScreen
from .input_callback import FuncCallback, InputCallback, ScreenCallback
from .callback_data import GoToScreen, RunFunc, StepBack, CallbackData
from .user_data import UserDataManager
from .user_screen import UserScreen
from .message import Message

class BotManager(ABC):
    def __init__(self):
        self.system_user_data: UserDataManager = None
        self.screen: UserScreen = None
        
    def config_delete_old_messages(self, user_id: int):
        input_callback = self.get_system_user_data(user_id).input_callback
        if input_callback is not None:
            return False
        return True
    
    def build(self):
        user_data = UserDataManager()
        screen = UserScreen(user_data)
        self.system_user_data = user_data
        self.screen = screen
        return self
    
    @abstractmethod
    def add_handlers(self): ...
    
    def get_system_user_data(self, user_id: int):
        return self.system_user_data.get(user_id)

    @abstractmethod
    def get_message_handler(self): ...

    async def _handle_message(self, user_id: int, **kwargs):
        user_data = self.get_system_user_data(user_id)
        delete_old: bool = self.config_delete_old_messages(user_id)
        if delete_old:
            await self.delete_message(**kwargs)
        
        input_callback: InputCallback = user_data.input_callback
        if input_callback is None:
            return
        
        await self.screen.clear(user_id, delete_old)
        
        if user_data.input_session:
            message = kwargs["message"]
            user_data.input_session.append(message)
        
        if isinstance(input_callback, FuncCallback):
            if input_callback.one_time:
                user_data.input_callback = None
            await input_callback.function(user_id=user_id
                , **input_callback.kwargs, **kwargs)
        elif isinstance(input_callback, ScreenCallback):
            user_data.input_callback = None
            await self.screen.set_by_name(user_id, input_callback.screen_name,
                input_callback.stack, **kwargs)
            

    @abstractmethod
    def get_callback_query_handler(self): ...
    
    @abstractmethod
    async def delete_message(self, message): ...
    
    async def mapping_key_error(self, user_id: int): ...
    
    async def _handle_callback_query(self, user_id: int, query_data: str):
        user_data = self.get_system_user_data(user_id)
        mapping = user_data.callback_mapping
        data: CallbackData = mapping.get_by_uuid(query_data)
        if data is None:
            await self.mapping_key_error(user_id)
            return
        
        if isinstance(data, GoToScreen):
            if data.pre_func:
                await data.pre_func(user_id)
            
            await self.screen.set_by_name(user_id, data.screen_name)
            
            if data.post_func:
                await data.post_func(user_id)
        
        elif isinstance(data, StepBack):
            if data.clear_input_callback:
                user_data.input_callback = None
            
            if data.pop_last_input and user_data.input_session:
                for i in range(data.times):
                    if user_data.input_session.messages == []:
                        break
                    user_data.input_session.messages.pop()
            
            if data.pre_func:
                await data.pre_func(user_id)
            
            await self.screen.step_back(user_id, data.times)
            
            if data.post_func:
                await data.post_func(user_id)
            
            user_data.update_input_session()
            
        elif isinstance(data, RunFunc):
            await data.function(user_id=user_id, **data.kwargs)
    
    def dynamic_screen(self, name: str):
        def decorator(func: Callable[[int],list[Message]]):
            self.screen.append_screen(DynamicScreen(name, func))
        return decorator


    
    
