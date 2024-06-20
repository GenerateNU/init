#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p python3Packages.typing python3Packages.inquirer python3Packages.typer python3Packages.rich python3Packages.pyfiglet

from cli import app

if __name__ == "__main__":
    app()
