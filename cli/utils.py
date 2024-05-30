from pathlib import Path

class File:
    def __init__(self, path: str, content: str = None) -> None:
        self.path: Path = Path(path)
        self.content: str = content

class Directory:
    def __init__(self, path: str) -> None:
        self.path: Path = Path(path)

class ValidationError(Exception):
    pass
