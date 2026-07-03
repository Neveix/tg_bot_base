from typing import Callable

from ...core.models.input_callback_use_params import InputCallbackUseParams
from ...core.interfaces import InputCallback


class FuncCallback(InputCallback):
    def __init__(
        self,
        function: Callable,
        one_time: bool = True,
        **kwargs,
    ):
        self.function = function
        self.one_time = one_time
        self.kwargs = kwargs

    async def use(
        self,
        *,
        params: InputCallbackUseParams,
    ) -> None:
        if self.one_time:
            params.user_state.input_callback = None

        await self.function(
            user_id=params.user_state.user_id,
            params=params,
            **self.kwargs,
        )


class ScreenCallback(InputCallback):
    def __init__(
        self,
        screen_name: str,
        stack: bool = False,
    ):
        self.screen_name = screen_name
        self.stack = stack

    async def use(
        self,
        *,
        params: InputCallbackUseParams,
    ) -> None:
        params.user_state.input_callback = None
        await params.screen_service.set(
            params.user_state.user_id,
            self.screen_name,
            self.stack,
        )
