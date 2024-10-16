from telegram import CallbackQuery
from .bot_manager import BotManager
from .evaluated_menu import EvaluatedMenu
from .evaluated_screen import EvaluatedScreen
from .screen import Screen

class UserScreenManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
    def get_user_screen(self, user_id: int) -> EvaluatedScreen | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        screen = self.bot_manager.user_local_data.get(user_id, "__screen")
        if screen is None:
            return None
        return [evaluated_menu.clone() for evaluated_menu in screen]
    def clear_user_screen(self, user_id: int):
        self.bot_manager.user_local_data.set(user_id, "__screen", None)
    async def set_user_screen(self, user_id: int, new_screen: EvaluatedScreen):
        """Sets the screen and send/edit messages.\n
new_screen must be not None here"""
        old_screen = self.get_user_screen(user_id)
        if old_screen is None or len(new_screen.menus) > len(old_screen.menus):
            self._pure_set_screen(user_id, new_screen)
            await self.send_screen(user_id, new_screen)
            return
        len_diff = len(old_screen.menus) - len(new_screen.menus)
        equal = True
        for i, new_menu in enumerate(new_screen.menus):
            if new_menu != old_screen[len_diff+i]:
                equal = False
                break
        if not equal:
            await self.edit_screen(user_id, new_screen)
    async def send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        for menu in new_screen.menus:
            await menu.send(self.bot_manager.bot, chat_id = user_id)
    async def edit_screen(self, user_id: int, new_screen: EvaluatedScreen):
        old_screen = self.get_user_screen(user_id)
        len_diff = len(old_screen.menus) - len(new_screen.menus)
        from .evaluated_menu import EvaluatedMenuHasNotSendedMessage
        for i, new_menu in enumerate(new_screen.menus):
            if old_screen[len_diff+i].sended_message is None:
                old_menu = old_screen[len_diff+i]
                raise EvaluatedMenuHasNotSendedMessage(old_menu)
            message_id = old_screen[len_diff+i].sended_message.id
            await new_menu.edit_message(self.bot_manager.bot, user_id, message_id)
    def _pure_set_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        self.bot_manager.user_local_data.set(user_id, "__screen", new_screen)
    async def switch_by_name(self, screen_name: str, query: CallbackQuery) -> None:
        screen = self.bot_manager.screen_manager.get_screen(screen_name)
        await self.switch(screen, query)
    async def switch(self, screen: Screen, query: CallbackQuery) -> None:
        user_id = query.from_user.id
        __directory_stack = self.bot_manager.user_local_data.get(user_id,"__directory_stack", [])
        if __directory_stack[-1] != screen.name:
            __directory_stack.append(screen.name)
        evaluated_menu = screen.to_evaluated_menu(bot_manager=self.bot_manager, user_id=user_id)
        await self.bot_manager.screen_manager.set_screen(user_id, new_screen=[evaluated_menu])
    async def step_back(self, query: CallbackQuery) -> None:
        user_id = query.from_user.id
        directory_stack = self.bot_manager.user_local_data.get(user_id, "__directory_stack")
        if len(directory_stack) == 1:
            return
        directory_stack.remove(directory_stack[-1])
        menu = self.bot_manager.button_manager.get_clone(directory_stack[-1])
        evaluated_menu = menu.to_evaluated_menu(bot_manager=self.bot_manager, user_id=user_id)
        await self.bot_manager.screen_manager.set_screen(user_id, new_screen=[evaluated_menu])