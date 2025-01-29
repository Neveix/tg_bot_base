from typing import Any


class InputMediaPhoto:
    def __init__(
             self 
            ,media: str | Any
            ,filename: str = None
            ,caption: str = None
            ,parse_mode: str = None
        ):
        self.media = media
        self.filename = filename
        self.caption = caption
        self.parse_mode = parse_mode