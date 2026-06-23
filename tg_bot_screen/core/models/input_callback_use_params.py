from dataclasses import dataclass

from tg_bot_screen.core.interfaces import ScreenService
from tg_bot_screen.core.models.user_state import UserState


@dataclass(frozen=True)
class InputCallbackUseParams:
    user_state: UserState
    screen_service: ScreenService

