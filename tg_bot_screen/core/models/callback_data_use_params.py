from dataclasses import dataclass
from typing import Callable, Sequence
from .session import InputSession


@dataclass(frozen=True)
class CallbackDataUseParams:
    user_id: int
    input_sessions: Sequence[InputSession]
    screen_set_by_name: Callable
    screen_step_back: Callable
    reset_input_callback: Callable
    update_sessions: Callable