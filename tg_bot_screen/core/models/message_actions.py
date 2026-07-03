from dataclasses import dataclass

from tg_bot_screen.core.interfaces import MessageDeleter, MessageEditor, MessageSender


@dataclass(kw_only=True)
class MessageActions:
    sender: MessageSender
    editor: MessageEditor
    deleter: MessageDeleter
