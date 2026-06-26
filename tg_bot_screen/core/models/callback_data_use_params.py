from dataclasses import dataclass
from typing import Protocol, Sequence
from .session import InputSession


class ScreenSetByName(Protocol):
    async def __call__(
        self,
        user_id: int,
        screen_name: str,
        stack: bool = True,
        **kwargs,
    ) -> None: ...


class ScreenStepBack(Protocol):
    async def __call__(self, user_id: int, times: int) -> None: ...


class ResetInputCallback(Protocol):
    def __call__(self) -> None: ...


class UpdateSettions(Protocol):
    def __call__(self) -> None: ...


@dataclass(frozen=True)
class CallbackDataUseParams:
    user_id: int
    input_sessions: Sequence[InputSession]
    screen_set_by_name: ScreenSetByName
    screen_step_back: ScreenStepBack
    reset_input_callback: ResetInputCallback
    update_sessions: UpdateSettions

