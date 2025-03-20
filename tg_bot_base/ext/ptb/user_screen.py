from asyncio import gather
from telegram import Bot

from ...screen import ReadyScreen
from .screen import SentScreen
from ...user_data import UserData
from ...user_screen import UserScreen as BaseUserScreen

class UserScreen(BaseUserScreen):
    def __init__(self, user_data: UserData, bot: Bot):
        super().__init__(user_data)
        self.bot = bot
    
    async def clear(self, user_id: int, delete_messages: bool):
        user_data = self.user_data.get(user_id)
        screen = user_data.screen
        if screen and delete_messages:
            await screen.delete(self.bot)
        user_data.screen = None
    
    async def set(self, user_id: int, new_screen: ReadyScreen):
        mapping = self._map_callback_data(user_id, new_screen)
        
        old_screen = self._get(user_id)
        user_data = self.user_data.get(user_id)
        delete, edit, send = self.calc_screen_difference(old_screen, new_screen)
        new_screen = SentScreen()
        tasks = []
        for message in delete:
            tasks.append( message.delete(self.bot) )
            
        for old_message, new_message in edit:
            old_message.change(new_message)
            tasks.append( old_message.edit(self.bot, mapping) )
            new_screen.extend([old_message])
        
        for message in send:
            new_message = await message.send(user_id, self.bot, mapping)
            new_screen.extend([new_message])
            
        await gather(*tasks)
        
        user_data.screen = new_screen