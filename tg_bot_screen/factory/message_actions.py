from tg_bot_screen.core.models.message_actions import MessageActions
from tg_bot_screen.infrastructure.message_sender import MessageSenderImpl
from tg_bot_screen.infrastructure.message_editor import MessageEditorImpl
from tg_bot_screen.infrastructure.message_deleter import MessageDeleterImpl


class MessageActionsFactory:
    def create(self) -> MessageActions:
        return MessageActions(
            sender=MessageSenderImpl(),
            editor=MessageEditorImpl(),
            deleter=MessageDeleterImpl(),
        )
