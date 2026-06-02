from typing import Protocol

from ..core.interfaces import UserStateStore
from ..core.models.user_screen import UserScreen

class MessageHandlerSettings(Protocol):
    def is_old_messages_deleting_enabled(self, user_id: int, **kwargs) -> bool:
        ...


class DeleteMessage(Protocol):
    async def __call__(self, **kwargs):
        ...    



class MessageHandler:
    def __init__(self,
        user_state_store: UserStateStore,
        settings: MessageHandlerSettings,
        delete_message: DeleteMessage,
        user_screen: UserScreen,
    ):
        self.user_state_store = user_state_store
        self.settings = settings
        self.delete_message = delete_message
        self.user_screen = user_screen
        
    
    async def handle(self, user_id: int, **kwargs):
        user_data = self.user_state_store.get(user_id)
        delete_old: bool = self.settings.is_old_messages_deleting_enabled(
            user_id, **kwargs)
        if delete_old:
            await self.delete_message(**kwargs)
        
        input_callback = user_data.input_callback
        if input_callback is None:
            return
        
        await self.user_screen.clear(user_id, delete_old)
        
        for session in user_data.sessions.get_input_sessions():
            if not session.add_new_messages:
                continue
            message = kwargs["message"]
            session.append(message)
        
        await input_callback.use(
            user_id=user_id, user_data=user_data,
            screen_set_by_name=self.user_screen.set_by_name,
            **kwargs
        )