from abc import ABC, abstractmethod
from typing import Self

from ...callback_data import CallbackData
from ...button_rows import ButtonRows



class MessageCategory:
    SIMPLE = "simple"
    MEDIA = "media"
    VIDEO_NOTE = "video_note"
    

class HasButtonRows(ABC):
    def __init__(self, button_rows: ButtonRows | None = None):
        self.button_rows = button_rows
        
    @abstractmethod
    def get_reply_markup(self, *args, **kwargs):
        ...
    
    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()



class UnSentMessage(ABC):
    def __init__(self, text: str, category: str):
        self.text = text
        self.category = category
    
    @abstractmethod
    async def send(self, user_id: int) -> "SentMessage": ...
    
    @abstractmethod
    def __eq__(self, other: object) -> bool: 
        ...
    
    @abstractmethod
    def clone(self) -> Self: ...


class SentMessage(ABC):
    def __init__(self, text: str, category: str):
        self.text = text
        self.category = category
    
    @abstractmethod
    async def delete(self): ...
    
    @abstractmethod
    def __eq__(self, other: object) -> bool: 
        ...
    
    @abstractmethod
    def clone(self) -> Self: ...
    
    @abstractmethod
    def get_unsent(self): ...
    
    @abstractmethod
    async def edit(self, *args, **kwargs) -> Self: ...



class MediaMessage(HasButtonRows, ABC):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None,
        parse_mode: str | None = None,
    ):
        super().__init__(button_rows)
        self.text = text
        self.parse_mode = parse_mode
        self.caption = MessageCategory.MEDIA
    
    def __new__(cls, *args, **kwargs):
        assert \
            cls is not MediaMessage, \
            "MediaMessage cannot be created directly, only its subclasses"
        return super().__new__(cls)


class SimpleMessage(UnSentMessage):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None, 
        parse_mode: str | None = None,
    ):
        super().__init__(text, MessageCategory.SIMPLE)
        self.parse_mode = parse_mode
        self.button_rows = button_rows



class AudioMessage(MediaMessage, UnSentMessage): ...


class DocumentMessage(MediaMessage, UnSentMessage): ...


class PhotoMessage(MediaMessage, UnSentMessage): ...


class VideoMessage(MediaMessage, UnSentMessage): ...


class VideoNoteMessage(UnSentMessage):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(text, MessageCategory.VIDEO_NOTE)
        self.button_rows = button_rows


class SentAudioMessage(MediaMessage, SentMessage): ...


class SentDocumentMessage(MediaMessage, SentMessage): ...


class SentSimpleMessage(SentMessage):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None, 
        parse_mode: str | None = None,
    ):
        super().__init__(text, MessageCategory.SIMPLE)
        self.parse_mode = parse_mode
        self.button_rows = button_rows


class SentPhotoMessage(MediaMessage, SentMessage): ...


class SentVideoMessage(MediaMessage, SentMessage): ...


class SentVideoNoteMessage(SentMessage):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(text, MessageCategory.VIDEO_NOTE)
        self.button_rows = button_rows
