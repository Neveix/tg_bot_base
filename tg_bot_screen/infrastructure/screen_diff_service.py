from typing import TypeVar, cast

from tg_bot_screen.core.models.message import Message, SentMessage
from tg_bot_screen.core.models.screen import SentScreen, UnSentScreen
from .screen_abstract_diff import calc_abstract_difference

MsgType = TypeVar("MsgType", bound=Message)
SentMsgType = TypeVar("SentMsgType", bound=SentMessage)


def calc_screen_difference(
    screen1: SentScreen | None,
    screen2: UnSentScreen,
    _msg_type: type[MsgType],
    _sent_msg_type: type[SentMsgType],
) -> tuple[list[SentMsgType], list[tuple[SentMsgType, MsgType]], list[MsgType]]:

    messages1 = cast(list[SentMsgType], screen1.messages if screen1 else [])
    messages2 = cast(list[MsgType], screen2.messages)
    type_codes = get_type_codes(messages1 + messages2)
    screen1_codes: list[int] = [type_codes[message.category] for message in messages1]
    screen2_codes: list[int] = [type_codes[message.category] for message in messages2]

    indices_delete, indices_edit, indices_send = calc_abstract_difference(
        screen1_codes, screen2_codes
    )

    messages_delete: list[SentMsgType] = [messages1[index] for index in indices_delete]
    messages_edit: list[tuple[SentMsgType, MsgType]] = [
        (messages1[from_i], messages2[to_i]) for from_i, to_i in indices_edit
    ]
    messages_send: list[MsgType] = [messages2[index] for index in indices_send]
    return messages_delete, messages_edit, messages_send


def get_type_codes(messages: list[MsgType | SentMsgType]):
    type_codes = []
    for message in messages:
        type_codes.append(message.category)
    return {code: i for i, code in enumerate(type_codes)}
