from typing import Callable

class CallbackData:
    def __init__(self, action: str, *args, **kwargs):
        """base for several classes, deprecated to use manually"""
        self.action = action
        self.args = args
        self.kwargs = kwargs
    def clone(self) -> "CallbackData":
        return CallbackData(
            action = self.action,
            args = self.args,
            kwargs = self.kwargs
        )
    def __eq__(self, other: "CallbackData"):
        return (
            self.action == other.action and \
            self.args == other.args and \
            self.kwargs == other.kwargs
        )

class FunctionCallbackData(CallbackData):
    def __init__(self, function: Callable, *args, **kwargs):
        super().__init__('function', function, *args, **kwargs)

class MenuCallbackData(CallbackData):
    def __init__(self, menu: str, *args, **kwargs):
        super().__init__('menu', menu, *args, **kwargs)

class StepBackCallbackData(CallbackData):
    def __init__(self):
        "init without args"
        super().__init__('step_back')

class URLCallbackData(CallbackData):
    def __init__(self, url: str):
        "init without args"
        super().__init__('url', url=url)