from typing import Callable
import typer
from art import text2art
from pathlib import Path
from rich.console import Console
from templates import get_flake, MIT_LICENSE, PULL_REQUEST_TEMPLATE
from utils import Directory, File, ValidationError

stdout_console = Console()
stderr_console = Console(stderr=True)

startup_art = text2art("INIT", "speed")
stdout_console.print(f"[bold dodger_blue1]{startup_art}[/bold dodger_blue1]")

app = typer.Typer()

def validate_name(value: str) -> str:
    if not value or not value.strip():
        raise ValidationError("Name cannot be empty.")
    return value

def validate_path(value: str) -> Path:
    if not value or not value.strip():
        raise ValidationError("Path cannot be empty.")
    return Path(value)

def validate_pkgs(value: str) -> list[str]:
    if not value or not value.strip():
        raise ValidationError("Packages cannot be empty.")
    return value.split()

def prompt_with_validation(prompt_text: str, callback: Callable) -> str:
    while True:
        value = typer.prompt(prompt_text)
        try:
            return callback(value)
        except ValidationError as e:
            stderr_console.print(f"[bold red]Error:[/bold red] {e}")

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
def initialize_repo(
    name: str = typer.Option(
        None,
        help="Name of the repository"
    ),
    path: Path = typer.Option(
        None,
        help="Path to the repository"
    ),
    pkgs: str = typer.Option(
        None,
        help="List of packages to include in the flake.nix file"
    )
) -> None:
    
    if name is None:
        name = prompt_with_validation("Enter the name of the repository", validate_name)
    else:
        try:
            validate_name(name)
        except ValidationError as e:
            stderr_console.print(f"[bold red]Error:[/bold red] {e}")
            name = prompt_with_validation("Enter the name of the repository", validate_name)

    if path is None:
        path = prompt_with_validation("Enter the path to the repository", validate_path)
    else:
        try:
            validate_path(path)
        except ValidationError as e:
            stderr_console.print(f"[bold red]Error:[/bold red] {e}")
            path = prompt_with_validation("Enter the path to the repository", validate_path)

    if pkgs is None:
        pkgs = prompt_with_validation("Enter the packages to include in the flake.nix file separated by a single space", validate_pkgs)
    else:
        try:
            validate_pkgs(pkgs)
        except ValidationError as e:
            stderr_console.print(f"[bold red]Error:[/bold red] {e}")
            pkgs = prompt_with_validation("Enter the packages to include in the flake.nix file separated by a single space", validate_pkgs)
    
    BASE_PATH = path / name
    BASE_PATH.mkdir(parents=True, exist_ok=True)

    objects = [
        # root files
        File("flake.nix", get_flake(pkgs)),
        File("LICENSE", MIT_LICENSE),
        File(".gitignore"),
        File("README.md"),

        # .github
        Directory(".github/workflows"),
        File(".github/pull_request_template.md", PULL_REQUEST_TEMPLATE),

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
