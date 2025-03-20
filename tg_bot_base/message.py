from abc import ABC, abstractmethod
from typing import Any

from .callback_data import CallbackData
from .button_rows import ButtonRows

class SentMessage(ABC):
    @abstractmethod
    async def change(self, message: "Message"): ...
    
    @abstractmethod
    async def edit(self) -> "SentMessage": ...
    
    @abstractmethod
    async def delete(self): ...
    
    @abstractmethod
    def __eq__(self, other: "Message"): ...
    
    @abstractmethod
    def clone(self): ...

class Message(ABC):
    @abstractmethod
    async def send(self, user_id: int) -> SentMessage: ...
    
    @abstractmethod
    def __eq__(self, other: "Message"): ...
    
    @abstractmethod
    def clone(self) -> "Message": ...

    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()

class AudioMessage(Message):
    def __init__(self, audio: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.audio = audio
        self.category = "audio"

class DocumentMessage(Message):
    def __init__(self, document: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.document = document
        self.category = "document"

class SimpleMessage(Message):
    def __init__(self, text: str, button_rows: ButtonRows = None):
        self.text = text
        self.button_rows = button_rows
        self.category = "simple"

class PhotoMessage(Message):
    def __init__(self, photo: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.photo = photo
        self.category = "photo"

class VideoMessage(Message):
    def __init__(self, video: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video = video
        self.category = "video"

class VideoNoteMessage(Message):
    def __init__(self, video_note: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video_note = video_note
        self.category = "video_note"

class SentAudioMessage(SentMessage):
    def __init__(self, audio: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.audio = audio
        self.category = "audio"

class SentDocumentMessage(SentMessage):
    def __init__(self, document: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.document = document
        self.category = "document"
        

class SentSimpleMessage(SentMessage):
    def __init__(self, text: str, button_rows: ButtonRows = None):
        self.text = text
        self.button_rows = button_rows
        self.category = "simple"

class SentPhotoMessage(SentMessage):
    def __init__(self, photo: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.photo = photo
        self.category = "photo"

class SentVideoMessage(SentMessage):
    def __init__(self, video: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video = video
        self.category = "video"

class SentVideoNoteMessage(SentMessage):
    def __init__(self, video_note: Any, caption: str, button_rows: ButtonRows = None):
        self.caption = caption
        self.button_rows = button_rows
        self.video_note = video_note
        self.category = "video_note"
