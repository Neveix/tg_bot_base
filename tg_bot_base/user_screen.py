from typing import TYPE_CHECKING
from .evaluated_screen import EvaluatedScreen
from .evaluated_menu import EvaluatedMenuHasNotSendedMessage
if TYPE_CHECKING:
    from .bot_manager import BotManager

class UserScreenManager:
    def __init__(self, bot_manager: "BotManager"):
        self.bot_manager = bot_manager
    
    def clear(self, user_id: int):
        user_data = self.bot_manager.user_data_manager.get(user_id)
        user_data.screen = None
    
    async def set(self, user_id: int, new_screen: EvaluatedScreen):
        """Sets the screen and send/edit messages.\n
new_screen must be not None here"""
        # Получаем копию старого экрана
        old_screen = self._get(user_id)
        user_data = self.bot_manager.user_data_manager.get(user_id)
        
        if old_screen is None or len(new_screen.menus) > len(old_screen.menus):
            user_data.screen = new_screen
            await self._send_screen(user_id, new_screen)
            return

        await self._edit_screen(user_id, new_screen)
    
    async def set_by_name(self, user_id: int, screen_name: str):
        directory_stack = self.bot_manager.user_data_manager.get(user_id).directory_stack
        if len(directory_stack)==0 or directory_stack[-1] != screen_name:
            directory_stack.append(screen_name)
        screen = self.bot_manager.screen_manager.get_screen(screen_name)
        evaluated_screen = screen.to_evaluated_screen(bot_manager = self.bot_manager, user_id = user_id)
        await self.set(user_id, evaluated_screen)
    
    async def update(self, user_id: int):
        directory_stack = self.bot_manager.user_data_manager.get(user_id).directory_stack
        if len(directory_stack)==0:
            raise ValueError("directory_stack was of length 0")
        await self.set_by_name(user_id, directory_stack[-1])
    
    async def step_back(self, user_id: int) -> None:
        directory_stack = self.bot_manager.user_data_manager.get(user_id).directory_stack
        if len(directory_stack) <= 1:
            return
        directory_stack.pop()
        await self.set_user_screen_by_name(user_id, directory_stack[-1])
    
    def _get(self, user_id: int) -> EvaluatedScreen | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        screen: EvaluatedScreen = self.bot_manager.user_data_manager.get(user_id).screen
        if screen is None:
            return None
        return screen.clone()
    
    async def _send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        for menu in new_screen.menus:
            await menu.send_message(self.bot_manager, user_id)
    
    async def _edit_screen(self, user_id: int, new_screen: EvaluatedScreen):
        old_screen = self._get(user_id)
        len_diff = len(old_screen.menus) - len(new_screen.menus)
        for i, new_menu in enumerate(new_screen.menus):
            old_menu = old_screen.menus[len_diff+i]
            if old_menu.sended_message is None:
                raise EvaluatedMenuHasNotSendedMessage(old_menu)
            new_menu.sended_message = old_menu.sended_message
            if new_menu == old_menu:
                continue
            message_id = old_screen.menus[len_diff+i].sended_message.id
            await new_menu.edit_message(self.bot_manager, user_id, message_id)
        user_data = self.bot_manager.user_data_manager.get(user_id)
        user_data.screen.menus[-len(new_screen.menus):] = new_screen.menus
    