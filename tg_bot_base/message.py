from abc import ABC, abstractmethod
from typing import Any

from .callback_data import CallbackData

from .button_rows import ButtonRows

class SentMessage(ABC):    
    @abstractmethod
    async def edit(self, user_id: int): ...
    
    @abstractmethod
    async def delete(self, user_id: int): ...
    
    @abstractmethod
    def __eq__(self, other: "Message"): ...
    
    @abstractmethod
    def clone(self): ...

class Message(ABC):
    @abstractmethod
    async def send(self, user_id: int): ...
    
    @abstractmethod
    def __eq__(self, other: "Message"): ...
    
    @abstractmethod
    def clone(self) -> "Message": ...

    def prepare(self) -> dict[str, CallbackData]:
        print(f"Message {self} prepare called!")
        if self.button_rows is not None:
            self.button_rows: ButtonRows
            return self.button_rows.prepare()
        return {}

class AudioMessage(Message):
    def __init__(self, audio: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.audio = audio

class DocumentMessage(Message):
    def __init__(self, document: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.document = document

class SimpleMessage(Message):
    def __init__(self, text: str, button_rows: ButtonRows = None):
        self.text = text
        self.button_rows = button_rows

class PhotoMessage(Message):
    def __init__(self, photo: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.photo = photo

class VideoMessage(Message):
    def __init__(self, video: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video = video

class VideoNoteMessage(Message):
    def __init__(self, video_note: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video_note = video_note

class SentAudioMessage(Message):
    def __init__(self, audio: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.audio = audio

class SentDocumentMessage(Message):
    def __init__(self, document: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.document = document

class SentSimpleMessage(Message):
    def __init__(self, text: str, button_rows: ButtonRows = None):
        self.text = text
        self.button_rows = button_rows

class SentPhotoMessage(Message):
    def __init__(self, photo: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.photo = photo

class SentVideoMessage(Message):
    def __init__(self, video: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video = video

class SentVideoNoteMessage(Message):
    def __init__(self, video_note: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video_note = video_note
