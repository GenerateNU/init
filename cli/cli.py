#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.typing python3Packages.inquirer python3Packages.typer python3Packages.rich

import os
import sys
from typing import Callable
import inquirer
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from templates import get_flake, MIT_LICENSE, PULL_REQUEST_TEMPLATE
from utils import Directory, File, ValidationError, CustomTheme

app = typer.Typer(add_completion=False)
stdout_console = Console()
stderr_console = Console(stderr=True)

BACKEND_LANGUAGES = ['Python', 'Java', 'C++', 'Rust', 'Go', 'None']
FRONTEND_LANGUAGES = ['JavaScript', 'TypeScript', 'None']
DATABASES = ['PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'None']

def select_pkgs() -> str:
    bold_cyan_code = '\033[1;96m'
    reset_code = '\033[0m'

    try:
        questions = [
            inquirer.List('backend',
                message=f"{bold_cyan_code}Select the backend language{reset_code}",
                choices=BACKEND_LANGUAGES
            ),
            inquirer.List('frontend',
                message=f"{bold_cyan_code}Select the frontend language{reset_code}",
                choices=FRONTEND_LANGUAGES
            ),
            inquirer.List('database',
                message=f"{bold_cyan_code}Select the database{reset_code}",
                choices=DATABASES
            )
        ]
        answers = inquirer.prompt(questions, theme=CustomTheme(), raise_keyboard_interrupt=True)
        return [pkg for pkg in [answers['backend'], answers['frontend'], answers['database']] if pkg != 'None']
    except KeyboardInterrupt:
        stderr_console.print("[red]Aborted.[/red]")
        sys.exit(1)

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
    
# repeatedly prompt user for input and parse it until user confirms
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
def create_repo() -> None:
    startup_art = """
   _____  ____________
  /  _/ |/ /  _/_  __/
 _/ //    // /  / /   
/___/_/|_/___/ /_/    
"""
    stdout_console.print(f"[bold dodger_blue1]{startup_art}[/bold dodger_blue1]")

    # prompt user for repository name and path
    name = prompt_and_parse("Enter the name of the repository", parse_name)

    PKGS = select_pkgs()

    if Confirm.ask("[bold cyan]Do you want to create the repository in the current directory?[/bold cyan]"):
        path = Path(os.getcwd())
    else:
        path = prompt_and_parse("Enter the path to the repository", parse_path)

    # define base path and create root directory
    BASE_PATH = path / name
    BASE_PATH.mkdir(parents=True, exist_ok=True)

    # list of predefined objects to create
    objects = [
        # root files
        File("flake.nix", content=get_flake(PKGS)),
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
