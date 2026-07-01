from io import BytesIO

from telegram import (
    InputFile,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
)

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
    def to_send_parameter(self, photo: Photo):
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

    def to_input_media(self, photo: Photo):
        send_param = self.to_send_parameter(photo)
        return InputMediaPhoto(media=send_param)


class AudioConverterPtb:
    def to_send_parameter(self, audio: Audio):
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

    def to_input_media(self, audio: Audio):
        send_param = self.to_send_parameter(audio)
        return InputMediaAudio(media=send_param)


class VideoConverterPtb:
    def to_send_parameter(self, video: Video):
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

    def to_input_media(self, video: Video):
        send_param = self.to_send_parameter(video)
        return InputMediaVideo(media=send_param)


class DocumentConverterPtb:
    def to_send_parameter(self, document: Document):
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

    def to_input_media(self, document: Document):
        send_param = self.to_send_parameter(document)
        return InputMediaDocument(media=send_param)


class VoiceConverterPtb:
    def to_send_parameter(self, voice: Voice):
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

    def to_input_media(self, voice: Voice):
        send_param = self.to_send_parameter(voice)
        return InputMediaAudio(media=send_param)


class VideoNoteConverterPtb:
    def to_send_parameter(self, video_note: VideoNote):
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


class GeneralConverterPtb:
    def __init__(self):
        self._photo_converter = PhotoConverterPtb()
        self._audio_converter = AudioConverterPtb()
        self._video_converter = VideoConverterPtb()
        self._document_converter = DocumentConverterPtb()
        self._voice_converter = VoiceConverterPtb()
        self._video_note_converter = VideoNoteConverterPtb()

    def to_send_parameter(
        self, media: Photo | Audio | Video | Document | Voice | VideoNote
    ):
        if isinstance(media, Photo):
            return self._photo_converter.to_send_parameter(media)

        if isinstance(media, Audio):
            return self._audio_converter.to_send_parameter(media)

        if isinstance(media, Video):
            return self._video_converter.to_send_parameter(media)

        if isinstance(media, Document):
            return self._document_converter.to_send_parameter(media)

        if isinstance(media, Voice):
            return self._voice_converter.to_send_parameter(media)

        if isinstance(media, VideoNote):
            return self._video_note_converter.to_send_parameter(media)

    def to_input_media(self, media: Photo | Audio | Video | Document | Voice):
        if isinstance(media, Photo):
            return self._photo_converter.to_input_media(media)

        if isinstance(media, Audio):
            return self._audio_converter.to_input_media(media)

        if isinstance(media, Video):
            return self._video_converter.to_input_media(media)

        if isinstance(media, Document):
            return self._document_converter.to_input_media(media)

        if isinstance(media, Voice):
            return self._voice_converter.to_input_media(media)
