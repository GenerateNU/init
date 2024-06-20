from pathlib import Path


class File:
    def __init__(self, *, name: str, content: str = "") -> None:
        self.__name: str = name
        self.__content: str = content

    def create(self, *, path: Path) -> None:
        file_path: Path = path / self.__name
        file_path.write_text(self.__content)


class Directory:
    def __init__(self, *, name: str, children: list["File | Directory"] = []) -> None:
        self.__name: str = name
        self.__children: list["File | Directory"] = children

    def create(self, *, path: Path) -> None:
        dir_path: Path = path / self.__name
        dir_path.mkdir()
        for child in self.__children:
            child.create(path=dir_path)
