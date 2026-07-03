from tg_bot_screen.core.interfaces import BotAdapter
from tg_bot_screen.core.models.message_actions import MessageActions
from tg_bot_screen.infrastructure.message_sender import MessageSenderImpl
from tg_bot_screen.infrastructure.message_editor import MessageEditorImpl
from tg_bot_screen.infrastructure.message_deleter import MessageDeleterImpl


class MessageActionsFactory:
    def __init__(self, bot_adapter: BotAdapter):
        self.bot_adapter = bot_adapter

    def create(self) -> MessageActions:
        return MessageActions(
            sender=MessageSenderImpl(self.bot_adapter),
            editor=MessageEditorImpl(self.bot_adapter),
            deleter=MessageDeleterImpl(self.bot_adapter),
        )
