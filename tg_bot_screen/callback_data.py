from types import CoroutineType
from typing import Any, Callable
from abc import ABC, abstractmethod

class CallbackData(ABC):
    @abstractmethod
    def clone(self): ...

class Dummy(CallbackData):
    def clone(self):
        return Dummy()

class RunFunc(CallbackData):
    def __init__(self, function: Callable, **kwargs):
        """Использование:  
            function - Функция для выполнения при нажатии кнопки  
            **kwargs - keyword аргументы функции
        """
        assert isinstance(function, Callable)
        self.function = function
        self.kwargs = kwargs
    
    def clone(self):
        return RunFunc(self.function, **self.kwargs)
    
    def __eq__(self, other: "RunFunc"):
        return isinstance(other, RunFunc) and \
            self.function == other.function and self.kwargs == other.kwargs

class GoToScreen(CallbackData):
    def __init__(self, screen_name: str, *
            , pre_func: Callable[ [int], None ] = None
            , post_func: Callable[ [int], None ] = None):
        assert isinstance(screen_name, str)
        assert pre_func is None or isinstance(pre_func, Callable)
        assert post_func is None or isinstance(post_func, Callable)
        
        self.screen_name = screen_name
        self.pre_func = pre_func
        self.post_func = post_func
    
    def clone(self):
        return GoToScreen(self.screen_name)
    
    def __eq__(self, other: "GoToScreen"):
        return isinstance(other, GoToScreen) and \
            self.screen_name == other.screen_name

class StepBack(CallbackData):
    def __init__(self, times: int = 1, clear_input_callback: bool = True,
            pop_last_input: bool = True):
        self.times = times
        self.clear_input_callback = clear_input_callback
        self.pop_last_input = pop_last_input

    def clone(self):
        return StepBack()
    
    def __eq__(self, other: "StepBack"):
        return isinstance(other, StepBack)

class CallbackDataMapping:
    def __init__(self):
        self.items = []
    
    def add(self, callback: CallbackData, uuid: str):
        self.items.append((callback, uuid))
    
    def get_by_callback(self, callback: CallbackData):
        for i_callback, uuid in self.items:
            if callback == i_callback:
                return uuid
        raise KeyError(callback)
    
    def get_by_uuid(self, uuid: str):
        for callback, i_uuid in self.items:
            if uuid == i_uuid:
                return callback
        return None