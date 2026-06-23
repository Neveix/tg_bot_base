from ..core.interfaces import DirectoryStack


class DirectoryStackImpl(DirectoryStack):
    def __init__(self) -> None:
        self.__stack: list[str] = []

    def get_all(self) -> tuple[str, ...]:
        return tuple(self.__stack)

    def last(self) -> str | None:
        try:
            return self.__stack[-1]
        except IndexError:
            return None

    def append(self, directory: str):
        self.__stack.append(directory)

    def pop(self):
        self.__stack.pop()

    def clear(self):
        self.__stack.clear()

    def __len__(self):
        return len(self.__stack)

