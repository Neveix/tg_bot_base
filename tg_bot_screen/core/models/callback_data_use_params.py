from dataclasses import dataclass
from typing import Protocol, Sequence

from tg_bot_screen.core.models.input_callback import InputCallback
from .session import InputSession


class ScreenSetByName(Protocol):
    async def __call__(
        self,
        user_id: int,
        screen_name: str,
        stack: bool = True,
        raise_on_error: bool = True,
    ) -> None: ...


class ScreenStepBack(Protocol):
    async def __call__(self, user_id: int, times: int) -> None: ...


class SetInputCallback(Protocol):
    def __call__(self, value: InputCallback | None) -> None: ...


class UpdateSettions(Protocol):
    def __call__(self) -> None: ...


@dataclass(frozen=True)
class CallbackDataUseParams:
    user_id: int
    input_sessions: Sequence[InputSession]
    screen_service_set: ScreenSetByName
    screen_step_back: ScreenStepBack
    set_input_callback: SetInputCallback
    update_sessions: UpdateSettions
