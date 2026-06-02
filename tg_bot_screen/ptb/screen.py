from asyncio import gather
from telegram import Bot
from ..core.models.screen import UnSentScreen, SentScreen as BaseSentScreen

class SentScreen(BaseSentScreen):   
    def clone(self) -> "SentScreen":
        return SentScreen(*[message.clone() for message in self.messages])
     
    async def delete(self, bot: Bot):
        tasks = [message.delete(bot)
            for message in self.messages]
        await gather(*tasks)
    
    def get_unsent(self):
        return UnSentScreen(*[
            message.get_unsent() 
            for message in self.messages])