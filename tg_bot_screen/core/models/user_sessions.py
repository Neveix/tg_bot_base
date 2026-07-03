from typing import TypeVar

from .directory_stack import DirectoryStack

from .session import Session, InputSession, SessionDeleteContext
from ..guards import check_bad_value

SessionType = TypeVar("SessionType")


class UserSessions:
    def __init__(self, directory_stack: DirectoryStack):
        self.__sessions: dict[str, Session] = {}
        self.__ses_del_ctx: dict[str, SessionDeleteContext] = {}
        self.directory_stack = directory_stack

    def get_all(self):
        return tuple([item[1] for item in self.__sessions.items()])

    def get_input_sessions(self):
        result: list[InputSession] = []
        for session in self.get_all():
            if isinstance(session, InputSession):
                result.append(session)
        return tuple(result)

    def add(self, session: Session) -> bool:
        check_bad_value(session, Session, self, "session")
        if self.get(session.id):
            return False

        self.__ses_del_ctx[session.id] = SessionDeleteContext(
            directory_level=len(self.directory_stack),
            last_directory=self.directory_stack.last() or "",
        )
        self.__sessions[session.id] = session
        return True

    def get(self, id: str) -> Session | None:
        return self.__sessions.get(id)

    def update_all(self):
        new_dir_level = len(self.directory_stack)
        last_directory = self.directory_stack.last()

        delete = set()
        for session in self.get_all():
            if not session.delete_if_level_decreased:
                continue

            del_ctx = self.__ses_del_ctx.get(session.id)

            if del_ctx is None:
                print("update_all: del_ctx is None!")
                continue

            if not del_ctx.directory_level > new_dir_level:
                continue

            delete.add(session)

        for session in self.get_all():
            if not session.delete_if_last_dir_changed:
                continue

            del_ctx = self.__ses_del_ctx.get(session.id)

            if del_ctx is None:
                print("update_all: del_ctx is None!")
                continue

            if del_ctx.last_directory == last_directory:
                continue

            delete.add(session)

        for session in delete:
            self.delete_by_object(session)

    def delete_by_object(self, session: Session):
        self.delete(session.id)

    def delete(self, session_id: str) -> None:
        del self.__sessions[session_id]

