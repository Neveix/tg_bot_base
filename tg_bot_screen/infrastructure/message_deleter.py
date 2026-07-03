import asyncio

from ..core.models.message import SentMessage

from ..core.interfaces import BotAdapter, MessageDeleter


class MessageDeleterImpl(MessageDeleter):
    async def delete(
        self,
        message: SentMessage,
        bot_adapter: BotAdapter,
    ) -> bool:
        results = await asyncio.gather(
            *[
                bot_adapter.delete_message(message.user_id, message_id)
                for message_id in message.message_ids
            ]
        )

        return all(results)
