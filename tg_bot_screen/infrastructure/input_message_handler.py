from typing import Protocol

from ..core.models.input_callback import InputCallbackUseParams
from ..core.interfaces import UserStateStore, ScreenService


class MessageHandlerSettings(Protocol):
    def is_screen_clearing_enabled(self, user_id: int, **kwargs) -> bool: ...


class MessageHandler:
    def __init__(
        self,
        user_state_store: UserStateStore,
        screen_service: ScreenService,
        settings: MessageHandlerSettings,
    ):
        self.user_state_store = user_state_store
        self.screen_service = screen_service
        self.settings = settings

    async def handle(self, user_id: int, **kwargs):
        user_state = self.user_state_store.get(user_id)

        input_callback = user_state.input_callback
        if input_callback is None:
            return

        if self.settings.is_screen_clearing_enabled(user_id=user_id, **kwargs):
            await self.screen_service.clear(user_id, delete_messages=False)

        for session in user_state.sessions.get_input_sessions():
            if not session.add_new_messages:
                continue
            message = kwargs["message"]
            session.append(message)

        await input_callback.use(
            params=InputCallbackUseParams(
                user_id=user_id,
                set_input_callback=user_state.set_input_callback,
                screen_service_set=self.screen_service.set,
            ),
            message=kwargs["message"],
        )
