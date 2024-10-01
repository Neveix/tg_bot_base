from typing import Callable

class CallbackData:
    def __init__(self, action: str, *args, **kwargs):
        """action should be 'step_back' 'function' 'menu' 'show_alert'"""
        self.action = action
        self.args = args
        self.kwargs = kwargs

class FunctionCallbackData(CallbackData):
    def __init__(self, function: Callable, *args, **kwargs):
        super().__init__('function', function, *args, **kwargs)

class MenuCallbackData(CallbackData):
    def __init__(self, menu: str, *args, **kwargs):
        super().__init__('menu', menu, *args, **kwargs)

class StepBackCallbackData(CallbackData):
    def __init__(self):
        super().__init__('step_back')