from typing import Literal

class CallbackData:
    def __init__(self,action: Literal['button','step_back','function','show_alert'] | str, *args, **kwargs):
        if action == Literal['button']:
            action = 'button'
        if action == Literal['step_back']:
            action = 'step_back'
        if action == Literal['function']:
            action = 'function'
        if action == Literal['show_alert']:
            action = 'show_alert'
        self.action = action
        self.args = args
        self.kwargs = kwargs