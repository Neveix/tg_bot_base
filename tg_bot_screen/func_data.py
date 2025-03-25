from typing import Callable

class FuncData:
    def __init__(self, function: Callable[[int],None]
        , one_time: bool = True, **kwargs):
        self.function = function
        self.one_time = one_time
        self.kwargs = kwargs