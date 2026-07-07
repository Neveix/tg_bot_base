from io import BytesIO

from telegram import (
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
    def to_send_parameter(self, media: Photo):
        if isinstance(media, PhotoFileId):
            return media.file_id

        if isinstance(media, PhotoUrl):
            return media.url

        if isinstance(media, PhotoPath):
            return open(media.path, "rb")

        if isinstance(media, PhotoBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported photo type: {type(media)}")

    def to_input_media(self, media: Photo):
        send_param = self.to_send_parameter(media)
        return InputMediaPhoto(
            media=send_param,
            caption=media.caption,
            parse_mode=media.parse_mode,
            filename=media.filename,
        )


class AudioConverterPtb:
    def to_send_parameter(self, media: Audio):
        if isinstance(media, AudioFileId):
            return media.file_id

        if isinstance(media, AudioUrl):
            return media.url

        if isinstance(media, AudioPath):
            return open(media.path, "rb")

        if isinstance(media, AudioBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported audio type: {type(media)}")

    def to_input_media(self, media: Audio):
        send_param = self.to_send_parameter(media)
        return InputMediaAudio(
            media=send_param,
            caption=media.caption,
            parse_mode=media.parse_mode,
            title=media.title,
            filename=media.filename,
        )


class VideoConverterPtb:
    def to_send_parameter(self, media: Video):
        if isinstance(media, VideoFileId):
            return media.file_id

        if isinstance(media, VideoUrl):
            return media.url

        if isinstance(media, VideoPath):
            return open(media.path, "rb")

        if isinstance(media, VideoBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported video type: {type(media)}")

    def to_input_media(self, media: Video):
        send_param = self.to_send_parameter(media)
        return InputMediaVideo(
            media=send_param,
            caption=media.caption,
            parse_mode=media.parse_mode,
            filename=media.filename,
        )


class DocumentConverterPtb:
    def to_send_parameter(self, media: Document):
        if isinstance(media, DocumentFileId):
            return media.file_id

        if isinstance(media, DocumentUrl):
            return media.url

        if isinstance(media, DocumentPath):
            return open(media.path, "rb")

        if isinstance(media, DocumentBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported document type: {type(media)}")

    def to_input_media(self, media: Document):
        send_param = self.to_send_parameter(media)
        return InputMediaDocument(
            media=send_param,
            caption=media.caption,
            parse_mode=media.parse_mode,
            filename=media.filename,
        )


class VoiceConverterPtb:
    def to_send_parameter(self, media: Voice):
        if isinstance(media, VoiceFileId):
            return media.file_id

        if isinstance(media, VoiceUrl):
            return media.url

        if isinstance(media, VoicePath):
            return open(media.path, "rb")

        if isinstance(media, VoiceBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported voice type: {type(media)}")

    def to_input_media(self, media: Voice):
        send_param = self.to_send_parameter(media)
        return InputMediaAudio(
            media=send_param,
            caption=media.caption,
            parse_mode=media.parse_mode,
            filename=media.filename,
        )


class VideoNoteConverterPtb:
    def to_send_parameter(self, media: VideoNote):
        if isinstance(media, VideoNoteFileId):
            return media.file_id

        if isinstance(media, VideoNotePath):
            return open(media.path, "rb")

        if isinstance(media, VideoNoteBytes):
            if isinstance(media.data, bytes):
                data = BytesIO(media.data)
            else:
                data = media.data
            return data

        raise TypeError(f"Unsupported video note type: {type(media)}")


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
