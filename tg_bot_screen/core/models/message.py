from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Self

from .callback_data_impl import CallbackData
from .button_rows import ButtonRows



class MessageCategory(StrEnum):
    SIMPLE = "simple"
    MEDIA = "media"
    VIDEO_NOTE = "video_note"
    
class ParseMode(StrEnum):
    MARKDOWN = "markdown"
    HTML = "html"

    
class HasText(ABC):
    def __init__(self, *,
        text: str,
        parse_mode: ParseMode | None = None,
    ):
        self.text = text
        self.parse_mode = parse_mode


class HasButtonRows(ABC):
    def __init__(self, *, button_rows: ButtonRows | None = None):
        self.button_rows = button_rows
        
    @abstractmethod
    def get_reply_markup(self, *args, **kwargs):
        ...
    
    def get_callback_data(self) -> list[CallbackData]:
        if self.button_rows is None:
            return []
        return self.button_rows.get_callback_data()



class UnSentMessage(HasButtonRows):
    def __init__(self, *,
        category: MessageCategory,
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(button_rows=button_rows)
        self.category = category
    
    @abstractmethod
    async def send(self, user_id: int) -> "SentMessage": ...
    
    @abstractmethod
    def __eq__(self, other: object) -> bool: 
        ...
    
    @abstractmethod
    def clone(self) -> Self: ...


class SentMessage(HasButtonRows):
    def __init__(self, 
        category: MessageCategory,
        button_rows: ButtonRows | None = None
    ):
        super().__init__(button_rows=button_rows)
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



class MediaMessage(HasText, HasButtonRows):
    def __init__(self, *,
        text: str, 
        button_rows: ButtonRows | None = None,
        parse_mode: ParseMode | None = None,
    ):
        HasText.__init__(self, text=text, parse_mode=parse_mode)
        HasButtonRows.__init__(self, button_rows=button_rows)
        self.category: MessageCategory = MessageCategory.MEDIA
    
    def __new__(cls, *args, **kwargs):
        assert \
            cls is not MediaMessage, \
            f"{cls.__name__} cannot be created directly, only its subclasses"
        return super().__new__(cls)


class SimpleMessage(UnSentMessage, HasText):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None, 
        parse_mode: ParseMode | None = None,
    ):
        UnSentMessage.__init__(self, button_rows=button_rows, category=MessageCategory.SIMPLE)
        HasText.__init__(self, text=text, parse_mode=parse_mode)
        




class AudioMessage(MediaMessage, UnSentMessage): ...


class DocumentMessage(MediaMessage, UnSentMessage): ...


class PhotoMessage(MediaMessage, UnSentMessage): ...


class VideoMessage(MediaMessage, UnSentMessage): ...


class VideoNoteMessage(UnSentMessage):
    def __init__(self, 
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(
            category=MessageCategory.VIDEO_NOTE, 
            button_rows=button_rows,
        )


class SentAudioMessage(MediaMessage, SentMessage): ...


class SentDocumentMessage(MediaMessage, SentMessage): ...


class SentSimpleMessage(SentMessage, HasText):
    def __init__(self, 
        text: str, 
        button_rows: ButtonRows | None = None, 
        parse_mode: ParseMode | None = None,
    ):
        super().__init__(category=MessageCategory.SIMPLE, button_rows=button_rows)
        HasText.__init__(self, text=text, parse_mode=parse_mode)


class SentPhotoMessage(MediaMessage, SentMessage): ...


class SentVideoMessage(MediaMessage, SentMessage): ...


class SentVideoNoteMessage(SentMessage):
    def __init__(self, 
        button_rows: ButtonRows | None = None,
    ):
        super().__init__(MessageCategory.VIDEO_NOTE, button_rows)
