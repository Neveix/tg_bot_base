from abc import ABC, abstractmethod
from email import message
from typing import Type
from uuid import uuid4

from .callback_data import CallbackDataMapping
from .screen import ProtoScreen, SentScreen
from .message import Message, SentMessage
from .user_data import UserDataManager
from .screen import ReadyScreen

class UserScreen(ABC):
    def __init__(self, user_data: UserDataManager):
        self.user_data = user_data
        self.screen_dict: dict[str, ProtoScreen] = {}
    
    def append_screen(self, screen: ProtoScreen):
        self.screen_dict[screen.name] = screen
    
    def extend_screen(self, screens: list[ProtoScreen]):
        for screen in screens:
            self.append_screen(screen)
    
    @abstractmethod
    async def clear(self, user_id: int, delete_messages: bool): ...
    
    async def set_by_name(self, user_id: int, screen_name: str):
        user_data = self.user_data.get(user_id)
        directory_stack = user_data.directory_stack
        if len(directory_stack)==0 or directory_stack[-1] != screen_name:
            directory_stack.append(screen_name)
        
        screen = self.screen_dict.get(screen_name)
        evaluated_screen = screen.evaluate()
        
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
    
    def get(self, user_id: int) -> SentScreen | None:
        screen = self.user_data.get(user_id).screen
        if screen is None:
            return None
        return screen.clone()
    
    def _map_callback_data(self, user_id: int, screen: ReadyScreen
            ) -> CallbackDataMapping:
        mapping = CallbackDataMapping()
        callback_data_list = screen.get_callback_data()
        for callback_data in callback_data_list:
            uuid = str(uuid4())
            mapping.add(callback_data, uuid)
        self.user_data.get(user_id).callback_mapping = mapping
        return mapping
        
    @abstractmethod
    async def set(self, user_id: int, new_screen: ReadyScreen):
        ...
    
    @staticmethod
    def calc_screen_difference(screen1: SentScreen, screen2: ReadyScreen):
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
    return indices_delete, indices_edit, indices_send