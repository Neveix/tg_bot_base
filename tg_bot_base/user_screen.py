from abc import ABC, abstractmethod
from email import message
from typing import Type
from .screen import Screen
from .message import Message, SentMessage
from .user_data import UserDataManager
from .evaluated_screen import EvaluatedScreen

class UserScreen(ABC):
    def __init__(self, user_data: UserDataManager):
        self.user_data = user_data
        self.screen_dict: dict[str, Screen] = {}
    
    def append_screen(self, screen: Screen):
        self.screen_dict[screen.name] = screen
    
    def extend_screen(self, screens: list[Screen]):
        for screen in screens:
            self.append_screen(screen)
    
    def clear(self, user_id: int):
        user_data = self.user_data.get(user_id)
        user_data.screen = None
    
    async def set_by_name(self, user_id: int, screen_name: str):
        user_data = self.user_data.get(user_id)
        directory_stack = user_data.directory_stack
        if len(directory_stack)==0 or directory_stack[-1] != screen_name:
            directory_stack.append(screen_name)
        
        screen = self.screen_dict.get(screen_name)
        evaluated_screen, callback_data_dict = screen.evaluate()
        
        user_data.callback_data = callback_data_dict
        # TODO: переместить callback_data в set или ещё куда-то
        
        await self.set(user_id, evaluated_screen)
    
    async def update(self, user_id: int):
        directory_stack = self.user_data.get(user_id).directory_stack
        if len(directory_stack) != 0:
            await self.set_by_name(user_id, directory_stack[-1])
    
    async def step_back(self, user_id: int) -> None:
        directory_stack = self.user_data.get(user_id).directory_stack
        if len(directory_stack) <= 1:
            return
        directory_stack.pop()
        await self.set_by_name(user_id, directory_stack[-1])
    
    def _get(self, user_id: int) -> EvaluatedScreen | None:
        screen: EvaluatedScreen = self.user_data.get(user_id).screen
        if screen is None:
            return None
        return screen.clone()
    
    @abstractmethod
    async def _send_screen(self, user_id: int, new_screen: EvaluatedScreen):
        ...
        
    @abstractmethod
    async def set(self, user_id: int, new_screen: EvaluatedScreen):
        ...
    
    @staticmethod
    def calc_screen_difference(screen1: EvaluatedScreen, screen2: EvaluatedScreen):
        messages1 = []
        if screen1:
            messages1 = screen1.messages
        messages2 = screen2.messages
        type_codes = get_type_codes(messages1 + messages2)
        screen1_codes = [type_codes[message.category] 
            for message in messages1]
        screen2_codes = [type_codes[message.category] 
            for message in messages2]
        
        indices_delete, indices_edit, indices_send = calc_abstract_difference(
            screen1_codes, screen2_codes)
        
        messages_delete: list[SentMessage] = [messages1[index]
            for index in indices_delete]
        messages_edit: list[tuple[SentMessage, Message]] = [
            (messages1[from_i],messages2[to_i])
            for from_i, to_i in indices_edit]
        messages_send: list[Message] = [messages2[index]
            for index in indices_send]
        return messages_delete, messages_edit, messages_send

SomeMessage = Message | SentMessage

def get_type_codes(messages: list[SomeMessage]):
    type_codes = set()
    for message in messages:
        type_codes.add(message.category)
    type_codes = list(type_codes)
    type_codes = [(code, i) for i, code in enumerate(type_codes)]
    return dict(type_codes)

def calc_abstract_difference(start: list[int], end: list[int]):
    indices_delete = []
    indices_edit = []
    indices_send = []
    startn = 0
    for j, enum in enumerate(end):
        if startn >= len(start):
            indices_send.append(j)
            continue
        for i, snum in enumerate(start[startn:], start=startn):
            startn += 1
            if enum == snum:
                # (from, to)
                indices_edit.append((i, j))
                break
            else:
                indices_delete.append(i)
        else:
            indices_send = end[j:]
            break
    indices_delete += list(range(startn,len(start)))
    # print(f"{start=}")
    # print(f"{end=}")
    # print(f"{indices_delete=}")
    # print(f"{indices_edit=}")
    # print(f"{indices_send=}")
    # print()
    return indices_delete, indices_edit, indices_send