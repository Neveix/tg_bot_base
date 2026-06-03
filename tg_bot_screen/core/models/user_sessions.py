from typing import Type, TypeVar

from .session import Session, InputSession
from .error_info import check_bad_value
from ...infrastructure.directory_stack import DirectoryStack

SessionType = TypeVar("SessionType")

class UserSessions:
    def __init__(self, directory_stack: DirectoryStack):
        self.__sessions: dict[str, Session] = {}
        self.directory_stack = directory_stack
    
    def get_all(self):
        return tuple([ item[1] for item in self.__sessions.items() ])
    
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
        
        session.directory_level = len(self.directory_stack)
        
        if last:=self.directory_stack.last():
            session.last_directory = last
        
        self.__sessions[session.id] = session
        return True
        
    def get(self, id: str, expected_class: Type[SessionType] = Session
            ) -> SessionType | None:
        return self.__sessions.get(id) # type: ignore
    
    def update_all(self):
        new_dir_level = len(self.directory_stack)
        last_directory = self.directory_stack.last()
        delete = []
        for session in self.get_all():
            if not session.delete_if_level_decreased:
                continue
            if not session.directory_level > new_dir_level:
                continue
            delete.append(session)
            
        for session in self.get_all():
            if not session.delete_if_last_dir_changed:
                continue
            if session.last_directory == last_directory:
                continue
            delete.append(session)
        
        for session in delete:
            self.delete(session)
    
    def delete(self, session: Session):
        check_bad_value(session, Session, self, "session")
        del self.__sessions[session.id]