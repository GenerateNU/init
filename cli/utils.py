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

STARTUP_ART = """
   _____  ____________
  /  _/ |/ /  _/_  __/
 _/ //    // /  / /   
/___/_/|_/___/ /_/    
"""

BACKEND_LANGUAGES = ['Python', 'Java', 'C++', 'Rust', 'Go', 'None']
FRONTEND_LANGUAGES = ['JavaScript', 'TypeScript', 'None']
DATABASES = ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'None']

NIX_PKGS_MAP = {
    'Python': ['python3'],
    'Java': ['openjdk'],
    'C++': ['gcc'],
    'Rust': ['rustup'],
    'Go': ['go'],
    'JavaScript': ['nodejs'],
    'TypeScript': ['typescript'],
    'PostgreSQL': ['postgresql'],
    'MySQL': ['mysql'],
    'SQLite': ['sqlite'],
    'MongoDB': ['mongodb'],
}