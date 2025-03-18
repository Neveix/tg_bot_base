from telegram import Bot
from ...evaluated_screen import EvaluatedScreen
from ...user_data import UserData
from ...user_screen import UserScreen as BaseUserScreen

class UserScreen(BaseUserScreen):
    def __init__(self, user_data: UserData, bot: Bot):
        super().__init__(user_data)
        self.bot = bot
    
    async def _send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        for message in new_screen.messages:
            await message.send(user_id, self.bot)