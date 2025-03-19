from asyncio import gather
from telegram import Bot

from tg_bot_base.message import Message
from ...evaluated_screen import EvaluatedScreen
from ...user_data import UserData
from ...user_screen import UserScreen as BaseUserScreen

class UserScreen(BaseUserScreen):
    def __init__(self, user_data: UserData, bot: Bot):
        super().__init__(user_data)
        self.bot = bot
    
    async def set(self, user_id: int, new_screen: EvaluatedScreen):
        old_screen = self._get(user_id)
        user_data = self.user_data.get(user_id)
        delete, edit, send = self.calc_screen_difference(old_screen, new_screen)
        new_screen = EvaluatedScreen()
        tasks = []
        for message in delete:
            tasks.append( message.delete(self.bot) )
            
        for old_message, new_message in edit:
            old_message.change(new_message)
            tasks.append( old_message.edit(self.bot) )
            new_screen.extend([old_message])
        
        for message in send:
            new_message = await message.send(user_id, self.bot)
            new_screen.extend([new_message])
            
        await gather(*tasks)
        
        user_data.screen = new_screen
    
    async def _send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        for message in new_screen.messages:
            await message.send(user_id, self.bot)