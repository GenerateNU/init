from inquirer.themes import Default, term
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

class CustomTheme(Default):
    def __init__(self):
        super().__init__()
        self.List.selection_color = term.yellow + term.bold
        self.List.unselected_color = term.gray40 + term.bold
