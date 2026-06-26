from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from io import BytesIO


@dataclass(kw_only=True)
class Photo(ABC):
    caption: str | None = None


@dataclass(kw_only=True)
class PhotoFileId(Photo):
    file_id: str


@dataclass(kw_only=True)
class PhotoUrl(Photo):
    url: str


@dataclass(kw_only=True)
class PhotoPath(Photo):
    path: Path | str


@dataclass(kw_only=True)
class PhotoBytes(Photo):
    data: bytes | BytesIO
    filename: str = "image.jpg"


# ----- #


@dataclass(kw_only=True)
class Audio(ABC):
    caption: str | None = None
    duration: int | None = None
    performer: str | None = None
    title: str | None = None


@dataclass(kw_only=True)
class AudioFileId(Audio):
    file_id: str


@dataclass(kw_only=True)
class AudioUrl(Audio):
    url: str


@dataclass(kw_only=True)
class AudioPath(Audio):
    path: Path | str


@dataclass(kw_only=True)
class AudioBytes(Audio):
    data: bytes | BytesIO
    filename: str = "audio.mp3"


# ----- #


@dataclass(kw_only=True)
class Video(ABC):
    caption: str | None = None
    duration: int | None = None
    width: int | None = None
    height: int | None = None
    supports_streaming: bool | None = None


@dataclass(kw_only=True)
class VideoFileId(Video):
    file_id: str


@dataclass(kw_only=True)
class VideoUrl(Video):
    url: str


@dataclass(kw_only=True)
class VideoPath(Video):
    path: Path | str


@dataclass(kw_only=True)
class VideoBytes(Video):
    data: bytes | BytesIO
    filename: str = "video.mp4"


# ----- #


@dataclass(kw_only=True)
class Document(ABC):
    caption: str | None = None


@dataclass(kw_only=True)
class DocumentFileId(Document):
    file_id: str


@dataclass(kw_only=True)
class DocumentUrl(Document):
    url: str


@dataclass(kw_only=True)
class DocumentPath(Document):
    path: Path | str


@dataclass(kw_only=True)
class DocumentBytes(Document):
    data: bytes | BytesIO
    filename: str = "document.pdf"


# ----- #


@dataclass(kw_only=True)
class Voice(ABC):
    duration: int | None = None
    "Длительность в секундах"


@dataclass(kw_only=True)
class VoiceFileId(Voice):
    file_id: str


@dataclass(kw_only=True)
class VoiceUrl(Voice):
    url: str


@dataclass(kw_only=True)
class VoicePath(Voice):
    path: Path | str


@dataclass(kw_only=True)
class VoiceBytes(Voice):
    data: bytes | BytesIO
    filename: str = "voice.ogg"


# ----- #


@dataclass(kw_only=True)
class VideoNote(ABC):
    duration: int | None = None
    "Длительность в секундах"
    length: int | None = None
    "Длина стороны видео (квадратное)"


@dataclass(kw_only=True)
class VideoNoteFileId(VideoNote):
    file_id: str


@dataclass(kw_only=True)
class VideoNotePath(VideoNote):
    path: Path | str


@dataclass(kw_only=True)
class VideoNoteBytes(VideoNote):
    data: bytes | BytesIO
    filename: str = "video_note.mp4"
