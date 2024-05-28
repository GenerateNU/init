import os
from typing import Callable
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from templates import get_flake, MIT_LICENSE, PULL_REQUEST_TEMPLATE
from utils import Directory, File, ValidationError

app = typer.Typer()
stdout_console = Console()
stderr_console = Console(stderr=True)

startup_art = """
   _____  ____________
  /  _/ |/ /  _/_  __/
 _/ //    // /  / /   
/___/_/|_/___/ /_/    

"""
stdout_console.print(f"[bold dodger_blue1]{startup_art}[/bold dodger_blue1]")

def parse_pkgs(val: str) -> list[str]:
    stripped_val = val.strip()
    if not stripped_val:
        raise ValidationError("Packages cannot be empty.")
    return stripped_val.split()

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
    
def prompt_and_parse(prompt_text: str, parse: Callable) -> str:
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
    pkgs: str = typer.Option(
        ...,
        help="List of packages to include in the flake.nix file"
    )
) -> None:
    
    pkgs = parse_pkgs(pkgs)
    name = prompt_and_parse("Enter the name of the repository", parse_name)
    if Confirm.ask("[bold cyan]Do you want to create the repository in the current directory?[/bold cyan]"):
        path = Path(os.getcwd())
    else:
        path = prompt_and_parse("Enter the path to the repository", parse_path)
    
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
