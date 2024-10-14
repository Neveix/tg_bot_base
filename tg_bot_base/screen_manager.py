
from .bot_manager import BotManager
from .evaluated_menu import EvaluatedMenu

class ScreenManager:
    def __init__(self, bot_manager: BotManager):
        self.bot_manager = bot_manager
    def get_screen(self, user_id: int) -> list[EvaluatedMenu] | None:
        """If self.screen is not None, returns copy if list of Evaluated Menus."""
        screen = self.bot_manager.user_local_data.get(user_id, "__screen")
        if screen is None:
            return None
        return [evaluated_menu.clone() for evaluated_menu in screen]
    def clear_screen(self, user_id: int):
        self.bot_manager.user_local_data.set(user_id, "__screen", None)
    async def set_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        """Sets the screen and send/edit messages.\n
new_screen must be not None here"""
        old_screen = self.get_screen(user_id)
        if old_screen is None or len(new_screen) > len(old_screen):
            self._pure_set_screen(user_id, new_screen)
            await self.send_screen(user_id, new_screen)
            return
        len_diff = len(old_screen) - len(new_screen)
        equal = True
        for i, new_menu in enumerate(new_screen):
            if new_menu != old_screen[len_diff+i]:
                equal = False
                break
        if not equal:
            await self.edit_screen(user_id, new_screen)
    async def send_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        for menu in new_screen:
            await menu.send(self.bot_manager.bot, chat_id = user_id)
    async def edit_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        old_screen = self.get_screen(user_id)
        len_diff = len(old_screen) - len(new_screen)
        from .evaluated_menu import EvaluatedMenuHasNotSendedMessage
        for i, new_menu in enumerate(new_screen):
            if old_screen[len_diff+i].sended_message is None:
                old_menu = old_screen[len_diff+i]
                print(f"{old_menu=}")
                print(f"{old_menu.sended_message=}")
                raise EvaluatedMenuHasNotSendedMessage(old_menu)
            message_id = old_screen[len_diff+i].sended_message.id
            await new_menu.edit_message(self.bot_manager.bot, user_id, message_id)
    def _pure_set_screen(self, user_id: int, new_screen: list[EvaluatedMenu]):
        self.bot_manager.user_local_data.set(user_id, "__screen", new_screen)