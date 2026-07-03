class TgBotScreenException(Exception):
    pass


class MessageNotModified(TgBotScreenException):
    pass


class BadRequest(TgBotScreenException):
    pass


class CannotTransformMessage(TgBotScreenException):
    pass


class ImplementationError(TgBotScreenException):
    pass


class ScreenAlreadyActiveError(TgBotScreenException):
    pass


class EmptyStackError(TgBotScreenException):
    pass


class ScreenNotFoundError(TgBotScreenException):
    pass


class NoScreenToUnbuffer(TgBotScreenException):
    pass
