class TgBotScreenException(Exception):
    pass


class MessageNotModified(TgBotScreenException):
    pass


class BadRequest(TgBotScreenException):
    pass


class CannotTransformMessage(TgBotScreenException):
    pass
