from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class ScreenServiceSetFunc(Protocol):
    async def __call__(
        self,
        user_id: int,
        screen_name: str,
        stack: bool = True,
        raise_on_error: bool = True,
    ) -> None: ...


class SetInputCallbackFunc(Protocol):
    def __call__(self, value: "InputCallback | None") -> None: ...


@dataclass(frozen=True)
class InputCallbackUseParams:
    set_input_callback: SetInputCallbackFunc
    user_id: int
    screen_service_set: ScreenServiceSetFunc


class InputCallback(ABC):
    @abstractmethod
    async def use(
        self,
        *,
        params: InputCallbackUseParams,
    ) -> None: ...


class FuncCallbackCallable(Protocol):
    async def __call__(self, user_id: int) -> None: ...


class FuncCallback(InputCallback):
    def __init__(
        self,
        function: FuncCallbackCallable,
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
            params.set_input_callback(None)

        await self.function(
            user_id=params.user_id,
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
        params.set_input_callback(None)
        await params.screen_service_set(
            params.user_id,
            self.screen_name,
            self.stack,
        )
