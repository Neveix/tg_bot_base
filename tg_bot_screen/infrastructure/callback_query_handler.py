from tg_bot_screen.core.exceptions import MappingKeyError
from tg_bot_screen.core.models.callback_data import CallbackData
from tg_bot_screen.core.models.callback_data_use_params import CallbackDataUseParams

from ..core.interfaces import UserStateStore
from ..core.interfaces import ScreenService


class CallbackQueryHandler:
    def __init__(
        self,
        user_state_store: UserStateStore,
        screen_service: ScreenService,
    ):
        self.user_state_store = user_state_store
        self.screen_service = screen_service

    async def handle(self, user_id: int, query_data: str, **kwargs):
        sud = self.user_state_store.get(user_id)
        mapping = sud.callback_mapping
        if mapping is None:
            return

        data: CallbackData | None = mapping.get_by_uuid(query_data)
        if data is None:
            raise MappingKeyError(f"can't find {query_data} for {user_id}")

        await data.use(
            params=CallbackDataUseParams(
                user_id=user_id,
                input_sessions=sud.sessions.get_input_sessions(),
                screen_service_set=self.screen_service.set,
                screen_step_back=self.screen_service.step_back,
                set_input_callback=sud.set_input_callback,
                update_sessions=sud.sessions.update_all,
            ),
            **kwargs,
        )
