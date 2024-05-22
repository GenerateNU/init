class File:
    def __init__(self, path: str, content: str = None) -> None:
        self.path: str = path
        self.content: str = content

class Directory:
    def __init__(self, path: str) -> None:
        self.path: str = path

class ValidationError(Exception):
    pass
