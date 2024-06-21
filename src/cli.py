import os
import sys
from typing import Callable
import inquirer
from inquirer.themes import Default, term
import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from tree import Directory
import templates
from options import Language, Service
from utils import to_lower_kebab_case, get_ascii_art, ValidationError

BACKEND_LANGUAGES: dict[str, set[Language]] = {
    "Go": {Language.GO},
    "TypeScript with pnpm": {Language.JAVASCRIPT_PNPM, Language.TYPESCRIPT},
    "TypeScript with Bun": {Language.JAVASCRIPT_BUN, Language.TYPESCRIPT},
    "Python": {Language.PYTHON},
    "Ruby": {Language.RUBY},
    "None": set(),
}
FRONTEND_LANGUAGES: dict[str, set[Language]] = {
    "TypeScript with pnpm": {Language.JAVASCRIPT_PNPM, Language.TYPESCRIPT},
    "TypeScript with Bun": {Language.JAVASCRIPT_BUN, Language.TYPESCRIPT},
    "None": set(),
}
SCRIPTING_LANGUAGES: dict[str, set[Language]] = {
    "Python": {Language.PYTHON},
    "Ruby": {Language.RUBY},
    "TypeScript with pnpm": {Language.JAVASCRIPT_PNPM, Language.TYPESCRIPT},
    "TypeScript with Bun": {Language.JAVASCRIPT_BUN, Language.TYPESCRIPT},
    "None": set(),
}
DATABASES: dict[str, set[Service]] = {
    "PostgreSQL": {Service.POSTGRESQL},
    "MongoDB": {Service.MONGODB},
    "MySQL": {Service.MYSQL},
    "None": set(),
}

app = typer.Typer(add_completion=False)
stdout_console = Console()
stderr_console = Console(stderr=True)


class CustomTheme(Default):
    def __init__(self):
        super().__init__()
        self.List.selection_color = term.yellow + term.bold
        self.List.unselected_color = term.gray40 + term.bold


def select_options() -> tuple[set[Language], set[Service]]:
    bold_cyan_code = "\033[1;96m"
    reset_code = "\033[0m"

    try:
        questions = [
            inquirer.List(
                "backend",
                message=f"{bold_cyan_code}Select a backend language{reset_code}",
                choices=[*BACKEND_LANGUAGES],
            ),
            inquirer.List(
                "frontend",
                message=f"{bold_cyan_code}Select a frontend language{reset_code}",
                choices=[*FRONTEND_LANGUAGES],
            ),
            inquirer.List(
                "scripting",
                message=f"{bold_cyan_code}Select a scripting language{reset_code}",
                choices=[*SCRIPTING_LANGUAGES],
            ),
            inquirer.List(
                "database",
                message=f"{bold_cyan_code}Select a database{reset_code}",
                choices=[*DATABASES],
            ),
        ]
        answers = inquirer.prompt(
            questions, theme=CustomTheme(), raise_keyboard_interrupt=True
        )
        return (
            BACKEND_LANGUAGES[answers["backend"]]
            | FRONTEND_LANGUAGES[answers["frontend"]]
            | SCRIPTING_LANGUAGES[answers["scripting"]],
            DATABASES[answers["database"]],
        )
    except KeyboardInterrupt:
        stderr_console.print("[red]Aborted.[/red]")
        sys.exit(1)


def parse_name(val: str) -> str:
    stripped_val = to_lower_kebab_case(val.strip())
    if not stripped_val:
        raise ValidationError("Name cannot be empty.")
    return stripped_val


def parse_description(val: str) -> str:
    stripped_val = val.strip()
    if not stripped_val:
        raise ValidationError("Description cannot be empty.")
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
            if Confirm.ask(
                f"[bold cyan]Are you sure you want to use[/bold cyan] [bold yellow]{parsed_value}[/bold yellow]?"
            ):
                return parsed_value
        except ValidationError as e:
            stderr_console.print(f"[red]Validation Error:[/red] {e}")


@app.command()
def create_repo() -> None:
    stdout_console.print(f"[bold cyan]{get_ascii_art('init')}[/bold cyan]")

    # prompt user for repository name and path
    name = prompt_and_parse("Enter the name of the repository", parse_name)
    description = prompt_and_parse(
        "Enter a short description of your project", parse_description
    )

    (languages, services) = select_options()
    if Confirm.ask(
        "[bold cyan]Do you want to create the repository in the current directory?[/bold cyan]"
    ):
        path = Path(os.getcwd())
    else:
        path = Path(prompt_and_parse("Enter the path to the repository", parse_path))

    # create any necessary parent directories
    path.mkdir(parents=True, exist_ok=True)

    # define and create directory tree
    Directory(
        name=name,
        children=[
            Directory(
                name=".github",
                children=[
                    Directory(
                        name="ISSUE_TEMPLATE",
                        children=[
                            templates.bug_report(),
                            templates.documentation_issue(),
                            templates.feature_request(),
                            templates.issue_config(),
                        ],
                    ),
                    Directory(name="workflows", children=[templates.ci()]),
                    templates.dependabot(),
                    templates.pull_request(),
                ],
            ),
            Directory(
                name="backend", children=[]
            ),  # TODO: define dirs and make conditional
            Directory(
                name="frontend", children=[]
            ),  # TODO: define dirs and make conditional
            templates.envrc(),
            templates.gitignore(),
            templates.flake(
                name=name,
                description=description,
                languages=languages,
                services=services,
            ),
            templates.license(),
            templates.readme(name=name, description=description),
        ],
    ).create(path=path)
