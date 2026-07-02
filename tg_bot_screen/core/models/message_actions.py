from dataclasses import dataclass

from tg_bot_screen.core.interfaces import MessageDeleter, MessageEditor, MessageSender


@dataclass(kw_only=True)
class MessageActions:
    send: MessageSender
    edit: MessageEditor
    delete: MessageDeleter
