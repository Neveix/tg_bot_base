from abc import ABC, abstractmethod
from typing import Any, Self

from .callback_data import CallbackData
from .button_rows import ButtonRows

class CanBeEdited(ABC):
    @abstractmethod
    async def change(self, message: "Message"): ...
    
    @abstractmethod
    async def edit(self) -> "CanBeEdited": ...

class SentMessage(ABC):
    def __init__(self):
        self.text: str = None
        self.category: str = None
    
    @abstractmethod
    async def delete(self): ...
    
    @abstractmethod
    def __eq__(self, other: Self): ...
    
    @abstractmethod
    def clone(self): ...
    
    @abstractmethod
    def get_unsent(self): ...

class Message(ABC):
    def __init__(self):
        self.category: str = None
    
    @abstractmethod
    async def send(self, user_id: int) -> SentMessage: ...
    
    @abstractmethod
    def __eq__(self, other: Self): ...
    
    @abstractmethod
    def clone(self) -> Self: ...

    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()

class AudioMessage(Message):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class DocumentMessage(Message):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class SimpleMessage(Message):
    def __init__(self, text: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.text = text
        self.button_rows = button_rows
        self.category = "simple"

class PhotoMessage(Message):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class VideoMessage(Message):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class VideoNoteMessage(Message):
    def __init__(self, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.category = "video_note"

class SentAudioMessage(SentMessage, CanBeEdited):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class SentDocumentMessage(SentMessage, CanBeEdited):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"
        

class SentSimpleMessage(SentMessage, CanBeEdited):
    def __init__(self, text: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.text = text
        self.button_rows = button_rows
        self.category = "simple"

class SentPhotoMessage(SentMessage, CanBeEdited):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class SentVideoMessage(SentMessage, CanBeEdited):
    def __init__(self, caption: str, button_rows: ButtonRows = None, 
            parse_mode: str = None):
        self.parse_mode = parse_mode
        self.caption = caption
        self.button_rows = button_rows
        self.category = "media"

class SentVideoNoteMessage(SentMessage):
    def __init__(self, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.category = "video_note"
