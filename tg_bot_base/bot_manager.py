from abc import abstractmethod, ABC
from .callback_data import GoToScreen, RunFunc, StepBack, CallbackData
from .user_data import UserDataManager
from .user_screen import UserScreen


class BotManager(ABC):
    def __init__(self):
        self.user_data: UserDataManager = None
        self.screen: UserScreen = None
        
    def build(self):
        user_data = UserDataManager()
        screen = UserScreen(user_data)
        self.user_data = user_data
        self.screen = screen
        return self

    @abstractmethod
    def get_message_handler(self): ...

    async def handle_message(self, user_id: int):
        user_data = self.user_data.get(user_id)
        self.screen.clear(user_id)
        
        after_input = user_data.after_input
        if after_input is not None:
            user_data.after_input = None
            await after_input(user_id=user_id)
            # TODO: Добавить kwargs и тип FuncData

    @abstractmethod
    def get_callback_query_handler(self): ...
    
    async def _handle_callback_query(self, user_id: int, query_data: str):
        callback_data = self.user_data.get(user_id).callback_data
        data: CallbackData = callback_data.get(query_data)
        if data is None:
            return
        
        if isinstance(data, GoToScreen):
            await self.screen.set_by_name(user_id, data.screen_name)
        
        elif isinstance(data, StepBack):
            await self.screen.step_back(user_id)
            
        elif isinstance(data, RunFunc):
            await data.function(user_id=user_id, **data.kwargs)
            
    


    
    
