from dataclasses import dataclass, field
from typing import Any, Protocol
from ...core.interfaces import CallbackData
from ...core.models.callback_data_use_params import CallbackDataUseParams


@dataclass(frozen=True)
class Dummy(CallbackData):
    def clone(self):
        return Dummy()

    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        pass


class RunFuncCallback(Protocol):
    async def __call__(self, *, user_id: int, params: CallbackDataUseParams, **kw): ...


@dataclass(frozen=True)
class RunFunc(CallbackData):
    function: RunFuncCallback
    func_kwargs: dict[str, Any] = field(default_factory=dict)
    "parameters user_id, params may cause an error"

    def clone(self):
        return RunFunc(self.function, **self.func_kwargs)

    async def use(self, *, params: CallbackDataUseParams):
        await self.function(user_id=params.user_id, params=params, **self.func_kwargs)


@dataclass(frozen=True)
class GoToScreen(CallbackData):
    screen_name: str

    def clone(self):
        return GoToScreen(self.screen_name)

    async def use(self, *, params: CallbackDataUseParams):
        await params.screen_set_by_name(params.user_id, self.screen_name)
        params.update_sessions()


@dataclass(frozen=True)
class StepBack(CallbackData):
    times: int = 1
    clear_input_callback: bool = True
    pop_last_input: bool = True

    def clone(self):
        return StepBack(
            self.times,
            self.clear_input_callback,
            self.pop_last_input,
        )

    async def use(self, *, params: CallbackDataUseParams, **kwargs):
        if self.clear_input_callback:
            params.reset_input_callback()

        for session in params.input_sessions:
            if self.pop_last_input and session.may_pop_last_input:
                for _ in range(self.times):
                    if not session.messages:
                        break
                    session.messages.pop()

        await params.screen_step_back(params.user_id, self.times)

        params.update_sessions()

