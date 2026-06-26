from io import BytesIO

from telegram import InputFile

from tg_bot_screen.core.models.media_data import (
    Audio,
    AudioBytes,
    AudioFileId,
    AudioPath,
    AudioUrl,
    Document,
    DocumentBytes,
    DocumentFileId,
    DocumentPath,
    DocumentUrl,
    Photo,
    PhotoBytes,
    PhotoFileId,
    PhotoPath,
    PhotoUrl,
    Video,
    VideoBytes,
    VideoFileId,
    VideoNote,
    VideoNoteBytes,
    VideoNoteFileId,
    VideoNotePath,
    VideoPath,
    VideoUrl,
    Voice,
    VoiceBytes,
    VoiceFileId,
    VoicePath,
    VoiceUrl,
)


class PhotoConverterPtb:
    def convert(self, photo: Photo):
        if isinstance(photo, PhotoFileId):
            return photo.file_id

        if isinstance(photo, PhotoUrl):
            return photo.url

        if isinstance(photo, PhotoPath):
            return InputFile(open(photo.path, "rb"))

        if isinstance(photo, PhotoBytes):
            if isinstance(photo.data, bytes):
                data = BytesIO(photo.data)
            else:
                data = photo.data
            return InputFile(data, filename=photo.filename)

        raise TypeError(f"Unsupported photo type: {type(photo)}")


class AudioConverterPtb:
    def convert(self, audio: Audio):
        if isinstance(audio, AudioFileId):
            return audio.file_id

        if isinstance(audio, AudioUrl):
            return audio.url

        if isinstance(audio, AudioPath):
            return InputFile(open(audio.path, "rb"))

        if isinstance(audio, AudioBytes):
            if isinstance(audio.data, bytes):
                data = BytesIO(audio.data)
            else:
                data = audio.data
            return InputFile(data, filename=audio.filename)

        raise TypeError(f"Unsupported audio type: {type(audio)}")


class VideoConverterPtb:
    def convert(self, video: Video):
        if isinstance(video, VideoFileId):
            return video.file_id

        if isinstance(video, VideoUrl):
            return video.url

        if isinstance(video, VideoPath):
            return InputFile(open(video.path, "rb"))

        if isinstance(video, VideoBytes):
            if isinstance(video.data, bytes):
                data = BytesIO(video.data)
            else:
                data = video.data
            return InputFile(data, filename=video.filename)

        raise TypeError(f"Unsupported video type: {type(video)}")


class DocumentConverterPtb:
    def convert(self, document: Document):
        if isinstance(document, DocumentFileId):
            return document.file_id

        if isinstance(document, DocumentUrl):
            return document.url

        if isinstance(document, DocumentPath):
            return InputFile(open(document.path, "rb"))

        if isinstance(document, DocumentBytes):
            if isinstance(document.data, bytes):
                data = BytesIO(document.data)
            else:
                data = document.data
            return InputFile(data, filename=document.filename)

        raise TypeError(f"Unsupported document type: {type(document)}")


class VoiceConverterPtb:
    def convert(self, voice: Voice):
        if isinstance(voice, VoiceFileId):
            return voice.file_id

        if isinstance(voice, VoiceUrl):
            return voice.url

        if isinstance(voice, VoicePath):
            return InputFile(open(voice.path, "rb"))

        if isinstance(voice, VoiceBytes):
            if isinstance(voice.data, bytes):
                data = BytesIO(voice.data)
            else:
                data = voice.data
            return InputFile(data, filename=voice.filename)

        raise TypeError(f"Unsupported voice type: {type(voice)}")


class VideoNoteConverterPtb:
    def convert(self, video_note: VideoNote):
        if isinstance(video_note, VideoNoteFileId):
            return video_note.file_id

        if isinstance(video_note, VideoNotePath):
            return InputFile(open(video_note.path, "rb"))

        if isinstance(video_note, VideoNoteBytes):
            if isinstance(video_note.data, bytes):
                data = BytesIO(video_note.data)
            else:
                data = video_note.data
            return InputFile(data, filename=video_note.filename)

        raise TypeError(f"Unsupported video note type: {type(video_note)}")
