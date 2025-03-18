from abc import ABC, abstractmethod
from .screen import Screen
from .user_data import UserDataManager
from .evaluated_screen import EvaluatedScreen

class UserScreen(ABC):
    def __init__(self, user_data: UserDataManager):
        self.user_data = user_data
        self.screen_dict: dict[str, Screen] = {}
    
    def append_screen(self, screen: Screen):
        self.screen_dict[screen.name] = screen
    
    def extend_screen(self, screens: list[Screen]):
        for screen in screens:
            self.append_screen(screen)
    
    def clear(self, user_id: int):
        user_data = self.user_data.get(user_id)
        user_data.screen = None
    
    async def set(self, user_id: int, new_screen: EvaluatedScreen):
        # Получаем копию старого экрана
        # old_screen = self._get(user_id)
        # user_data = self.user_data.get(user_id)
        
        await self._send_screen(user_id, new_screen)
    
    async def set_by_name(self, user_id: int, screen_name: str):
        user_data = self.user_data.get(user_id)
        directory_stack = user_data.directory_stack
        if len(directory_stack)==0 or directory_stack[-1] != screen_name:
            directory_stack.append(screen_name)
        
        screen = self.screen_dict.get(screen_name)
        evaluated_screen, callback_data_dict = screen.evaluate()
        
        user_data.callback_data = callback_data_dict
        
        await self.set(user_id, evaluated_screen)
    
    async def update(self, user_id: int):
        directory_stack = self.user_data.get(user_id).directory_stack
        if len(directory_stack) != 0:
            await self.set_by_name(user_id, directory_stack[-1])
    
    async def step_back(self, user_id: int) -> None:
        directory_stack = self.user_data.get(user_id).directory_stack
        if len(directory_stack) <= 1:
            return
        directory_stack.pop()
        await self.set_by_name(user_id, directory_stack[-1])
    
    def _get(self, user_id: int) -> EvaluatedScreen | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        screen: EvaluatedScreen = self.user_data.get(user_id).screen
        if screen is None:
            return None
        return screen.clone()
    
    @abstractmethod
    async def _send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        ...
    