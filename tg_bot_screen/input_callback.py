from abc import ABC, abstractmethod
from typing import Callable

from .user_data import UserData

class InputCallback(ABC): 
    @abstractmethod
    async def use(self, *, user_id: int, 
        user_data: UserData, 
        screen_set_by_name: Callable, **kw) -> None: ...


class FuncCallback(InputCallback):
    def __init__(self, function: Callable
        , one_time: bool = True, **kwargs):
        self.function = function
        self.one_time = one_time
        self.kwargs = kwargs
    
    def __call__(self, **kwds):
        return self.function(**self.kwargs, **kwds)
    
    async def use(self, *, user_id: int, 
            user_data: UserData, 
            screen_set_by_name: Callable, **kw) -> None:
        if self.one_time:
            user_data.input_callback = None
            
        await self.function(user_id=user_id
                , **self.kwargs, **kw)
        

class ScreenCallback(InputCallback):
    def __init__(self, screen_name: str, stack: bool = False):
        self.screen_name = screen_name
        self.stack = stack
        
    async def use(self, *, user_id: int, 
            user_data: UserData, 
            screen_set_by_name: Callable, **kw) -> None:
        user_data.input_callback = None
        await screen_set_by_name(user_id, self.screen_name,
            self.stack, **kw)