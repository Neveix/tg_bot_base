from asyncio import gather
from telegram import Bot
from ...screen import SentScreen as BaseSentScreen
from ...message import SentMessage

class SentScreen(BaseSentScreen):   
    def clone(self) -> "SentScreen":
        return SentScreen(*[message.clone() for message in self.messages])
     
    async def delete(self, bot: Bot):
        tasks = [message.delete(bot)
            for message in self.messages]
        await gather(*tasks)