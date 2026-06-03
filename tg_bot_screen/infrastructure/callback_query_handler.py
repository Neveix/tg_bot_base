from typing import Protocol

from ..core.interfaces import UserStateStore
from ..core.models.callback_data_impl import CallbackData, CallbackDataUseParams
from ..core.models.user_screen import UserScreen


class CallbackQueryHandlerSettings(Protocol):
    async def mapping_key_error_callback(self, user_id: int) -> None:
        ...

class CallbackQueryHandler:
    def __init__(self,
        user_state_store: UserStateStore,
        settings: CallbackQueryHandlerSettings,
        user_screen: UserScreen,
    ):
        self.user_state_store = user_state_store
        self.settings = settings
        self.user_screen = user_screen
    
    async def handle(self, user_id: int, query_data: str, **kwargs):
        sud = self.user_state_store.get(user_id)
        mapping = sud.callback_mapping
        data: CallbackData | None = mapping.get_by_uuid(query_data)
        if data is None:
            await self.settings.mapping_key_error_callback(user_id)
            return
        
        await data.use(
            params=CallbackDataUseParams(
                user_id=user_id,
                input_sessions=sud.sessions.get_input_sessions(),
                screen_set_by_name=self.user_screen.set_by_name,
                screen_step_back=self.user_screen.step_back,
                reset_input_callback=sud.reset_input_callback,
                update_sessions=sud.sessions.update_all,
            ),
            **kwargs
        )