import asyncio

from ..core.models.message import SentMessage
from ..core.interfaces import BotAdapter, MessageDeleter


class MessageDeleterImpl(MessageDeleter):
    def __init__(self, bot_adapter: BotAdapter):
        self.bot_adapter = bot_adapter

    async def delete(
        self,
        message: SentMessage,
    ) -> bool:
        results = await asyncio.gather(
            *[
                self.bot_adapter.delete_message(message.user_id, message_id)
                for message_id in message.message_ids
            ]
        )
        return all(results)
