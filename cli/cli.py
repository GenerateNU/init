import os
from typing import Callable
import inquirer
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from templates import get_flake, MIT_LICENSE, PULL_REQUEST_TEMPLATE
from utils import Directory, File, ValidationError

app = typer.Typer()
stdout_console = Console()
stderr_console = Console(stderr=True)

BACKEND_LANGUAGES = ['Python', 'Java', 'C++', 'Rust', 'Go', 'None']
FRONTEND_LANGUAGES = ['JavaScript', 'TypeScript', 'None']
DATABASES = ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'None']

def parse_backend(val: str) -> str:
    stripped_val = val.strip()
    if stripped_val not in BACKEND_LANGUAGES:
        raise ValidationError(f"Invalid backend language. Choose from {', '.join(BACKEND_LANGUAGES)}")
    return stripped_val

def parse_frontend(val: str) -> str:
    stripped_val = val.strip()
    if stripped_val not in FRONTEND_LANGUAGES:
        raise ValidationError(f"Invalid frontend language. Choose from {', '.join(FRONTEND_LANGUAGES)}")
    return stripped_val

def parse_database(val: str) -> str:
    stripped_val = val.strip()
    if stripped_val not in DATABASES:
        raise ValidationError(f"Invalid database. Choose from {', '.join(DATABASES)}")
    return stripped_val

def parse_name(val: str) -> str:
    stripped_val = val.strip()
    if not stripped_val:
        raise ValidationError("Name cannot be empty.")
    return stripped_val

def parse_path(val: str) -> Path:
    stripped_val = val.strip()
    if not stripped_val:
        raise ValidationError("Path cannot be empty.")
    return Path(stripped_val)

def prompt_select_and_parse(prompt_text: str, choices: list[str]) -> str:
    questions = [
        inquirer.List('choice',
            message=prompt_text,
            choices=choices
        )
    ]
    answers = inquirer.prompt(questions)
    return answers['choice']
    
# repeatedly prompt user for input and parse it until user confirms
def prompt_text_and_parse(prompt_text: str, parse: Callable) -> str:
    while True:
        value = Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]")
        try:
            parsed_value = parse(value)
            if Confirm.ask(f"[bold cyan]Are you sure you want to use[/bold cyan] [bold yellow]{value}[/bold yellow]?"):
                return parsed_value
        except ValidationError as e:
            stderr_console.print(f"[red]Validation Error:[/red] {e}")

def create_directories(directories: list[Directory], base_path: Path) -> None:
    for directory in directories:
        dir_path = base_path / directory.path
        dir_path.mkdir(parents=True, exist_ok=True)

def create_files(files: list[File], base_path: Path) -> None:
    for file in files:
        file_path = base_path / file.path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(file.content.strip() + "\n" if file.content else "")

@app.command()
def create_repo(
    backend: str = typer.Option(
        None,
        help="Backend language of choice"
    ),
    frontend: str = typer.Option(
        None,
        help="Frontend language of choice"
    ),
    database: str = typer.Option(
        None,
        help="Database of choice"
    ),
) -> None:
    startup_art = """
   _____  ____________
  /  _/ |/ /  _/_  __/
 _/ //    // /  / /   
/___/_/|_/___/ /_/    
"""
    stdout_console.print(f"[bold dodger_blue1]{startup_art}[/bold dodger_blue1]")

    if backend is None:
        backend = prompt_select_and_parse("Select the backend language", BACKEND_LANGUAGES)
    else:
        try:
            backend = parse_backend(backend)
        except ValidationError as e:
            stderr_console.print(f"[red]Validation Error:[/red] {e}")
            backend = prompt_select_and_parse("Select the backend language", BACKEND_LANGUAGES)

    if frontend is None:
        frontend = prompt_select_and_parse("Select the frontend language", FRONTEND_LANGUAGES)
    else:
        try:
            frontend = parse_frontend(frontend)
        except ValidationError as e:
            stderr_console.print(f"[red]Validation Error:[/red] {e}")
            frontend = prompt_select_and_parse("Select the frontend language", FRONTEND_LANGUAGES)

    if database is None:
        database = prompt_select_and_parse("Select the database", DATABASES)
    else:
        try:
            database = parse_database(database)
        except ValidationError as e:
            stderr_console.print(f"[red]Validation Error:[/red] {e}")
            database = prompt_select_and_parse("Select the database", DATABASES)
        
    PKGS = [backend, frontend, database]
    FILTERED_PKGS = [pkg for pkg in PKGS if pkg != "None"]

    # prompt user for repository name and path
    name = prompt_text_and_parse("Enter the name of the repository", parse_name)
    if Confirm.ask("[bold cyan]Do you want to create the repository in the current directory?[/bold cyan]"):
        path = Path(os.getcwd())
    else:
        path = prompt_text_and_parse("Enter the path to the repository", parse_path)
    
    # define base path and create root directory
    BASE_PATH = path / name
    BASE_PATH.mkdir(parents=True, exist_ok=True)

    # list of predefined objects to create
    objects = [
        # root files
        File("flake.nix", content=get_flake(FILTERED_PKGS)),
        File("LICENSE", content=MIT_LICENSE),
        File(".gitignore"),
        File("README.md"),

        # .github
        Directory(".github/workflows"),
        File(".github/pull_request_template.md", content=PULL_REQUEST_TEMPLATE),

        # backend
        Directory("backend/src"),

        # frontend
        Directory("frontend/src"),
        Directory("frontend/public"),
    ]

    directories = [obj for obj in objects if isinstance(obj, Directory)]
    files = [obj for obj in objects if isinstance(obj, File)]

    create_directories(directories, BASE_PATH)
    create_files(files, BASE_PATH)

if __name__ == "__main__":
    app()
