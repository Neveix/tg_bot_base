from dataclasses import dataclass
from typing import TypeVar

from tg_bot_screen.core.interfaces import MessageEditor
from tg_bot_screen.core.models.message import UnSentMessage, SentMessage
from tg_bot_screen.core.models.screen import SentScreen, UnSentScreen
from .message_abstract_diff import calc_abstract_difference

MsgType = TypeVar("MsgType", bound=UnSentMessage)
SentMsgType = TypeVar("SentMsgType", bound=SentMessage)


@dataclass
class ScreenDifference:
    delete: list[SentMessage]
    edit: list[tuple[SentMessage, UnSentMessage]]
    send: list[UnSentMessage]


def calc_screen_difference(
    screen1: SentScreen | None,
    screen2: UnSentScreen,
    message_editor: MessageEditor,
) -> ScreenDifference:

    messages1 = screen1.messages if screen1 else []
    messages2 = screen2.messages

    indices_delete, indices_edit, indices_send = calc_abstract_difference(
        messages1, messages2, message_editor.check_message_can_be_replaced
    )

    messages_delete: list[SentMessage] = [messages1[index] for index in indices_delete]
    messages_edit: list[tuple[SentMessage, UnSentMessage]] = [
        (messages1[from_i], messages2[to_i]) for from_i, to_i in indices_edit
    ]
    messages_send: list[UnSentMessage] = [messages2[index] for index in indices_send]

    return ScreenDifference(
        delete=messages_delete,
        edit=messages_edit,
        send=messages_send,
    )
