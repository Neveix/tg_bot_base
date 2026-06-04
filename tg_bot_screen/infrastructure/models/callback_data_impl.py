from dataclasses import dataclass, field
from typing import Callable, Self
from ...core.interfaces import CallbackData
from ...core.models.callback_data_use_params import CallbackDataUseParams
from .input_callback_impl import FuncCallback







@dataclass(frozen=True)
class Dummy(CallbackData):
    def clone(self):
        return Dummy()
    
    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        pass



@dataclass(frozen=True)
class RunFunc(CallbackData):
    function: Callable
    func_kwargs: dict = field(default_factory=dict)
    
    def clone(self):
        return RunFunc(self.function, **self.func_kwargs)
    
    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        await self.function(user_id=params.user_id, **self.func_kwargs, **kwargs)



@dataclass(frozen=True)
class GoToScreen(CallbackData):
    screen_name: str
    pre_func: FuncCallback | None = None
    post_func: FuncCallback | None = None
    
    def clone(self):
        return GoToScreen(self.screen_name, self.pre_func, self.post_func)
    
    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        if self.pre_func:
            await self.pre_func(user_id=params.user_id, **kwargs)
        await params.screen_set_by_name(params.user_id, self.screen_name, **kwargs)
        if self.post_func:
            await self.post_func(user_id=params.user_id, **kwargs)
        params.update_sessions()



@dataclass(frozen=True)
class StepBack(CallbackData):
    times: int = 1
    clear_input_callback: bool = True
    pop_last_input: bool = True
    pre_func: FuncCallback | None = None
    post_func: FuncCallback | None = None
    
    def clone(self):
        return StepBack(self.times, self.clear_input_callback, 
                        self.pop_last_input, self.pre_func, self.post_func)
    
    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        if self.clear_input_callback:
            params.reset_input_callback()
        
        for session in params.input_sessions:
            if self.pop_last_input and session.may_pop_last_input:
                for _ in range(self.times):
                    if not session.messages:
                        break
                    session.messages.pop()
        
        if self.pre_func:
            await self.pre_func(user_id=params.user_id, **kwargs)
        
        await params.screen_step_back(params.user_id, self.times)
        
        if self.post_func:
            await self.post_func(user_id=params.user_id, **kwargs)
        
        params.update_sessions()