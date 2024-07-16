from typing import Callable

class Operation:
    def __init__(self, name: str, inputs_count: int = 1, actions: list[str | Callable] = []):
        self.name = name
        self.inputs_count = inputs_count
        self.actions = actions
        self.operation_manager = None
    def get_action(self, action_index: int = 0, **kwargs):
        action = self.actions[action_index]
        if callable(action):
            action = action(**kwargs)
        return action