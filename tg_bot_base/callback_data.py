from typing import Callable
from abc import ABC, abstractmethod

class CallbackData(ABC):
    @abstractmethod
    def clone(self): ...

class RunFunc(CallbackData):
    def __init__(self, function: Callable, **kwargs):
        """Использование:  
            function - Функция для выполнения при нажатии кнопки  
            **kwargs - keyword аргументы функции
        """
        if not isinstance(function, Callable):
            raise ValueError(f"{function=} is not Callable")
        self.function = function
        self.kwargs = kwargs
    
    def clone(self):
        return RunFunc(self.function, **self.kwargs)
    
    def __eq__(self, other: "RunFunc"):
        return isinstance(other, RunFunc) and \
            self.function == other.function and self.kwargs == other.kwargs
        

class GoToScreen(CallbackData):
    def __init__(self, screen_name: str):
        if not isinstance(screen_name, str):
            raise ValueError(f"{screen_name=} is not str")
        self.screen_name = screen_name
    
    def clone(self):
        return GoToScreen(self.screen_name)
    
    def __eq__(self, other: "GoToScreen"):
        return isinstance(other, GoToScreen) and \
            self.screen_name == other.screen_name

class StepBack(CallbackData):
    pass

    def clone(self):
        return StepBack()
    
    def __eq__(self, other: "StepBack"):
        return isinstance(other, StepBack)

# class URLCallbackData(CallbackData):
#     def __init__(self, url: str):
#         self.url = url

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
        raise KeyError(uuid)