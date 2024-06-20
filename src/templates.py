from datetime import datetime
from options import Language, Service, NixOption
from tree import File
from utils import get_ascii_art


def bug_report() -> File:
    return File(
        name="bug_report.yaml",
        content="""---
name: 🐛 Bug Report
description: Report a bug that should be fixed
labels: [bug]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for submitting a bug report! It helps make `pxl` better.

        Make sure you are using the latest version of `pxl`.
        The bug you are experiencing may already have been fixed.

        Please try to include as much information as possible!

  - type: input
    attributes:
      label: What version of `pxl` are you using?
  - type: textarea
    attributes:
      label: What is the expected behavior?
      description: Please provide text instead of a screenshot.
    validations:
      required: true
  - type: textarea
    attributes:
      label: What is the actual behavior?
      description: Please provide text instead of a screenshot.
    validations:
      required: true
  - type: textarea
    attributes:
      label: What steps will reproduce the bug?
      description: Explain the steps and provide a code snippet that can reproduce it.
    validations:
      required: true
  - type: textarea
    attributes:
      label: Additional information
      description: Is there anything else you think we should know?
...
""",
    )


def ci() -> File:
    return File(
        name="ci.yaml",
        content="""---
name: ci

on:
  pull_request:
    branches:
      - "main"
  push:
    branches:
      - "*"
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    strategy:
      matrix:
        os: [ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - name: check out repository
        uses: actions/checkout@v4
      - name: install Nix
        uses: DeterminateSystems/nix-installer-action@main
      - name: activate devshell
        run: nix develop
      - name: lint
        run: echo TODO && exit 1
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - name: check out repository
        uses: actions/checkout@v4
      - name: install Nix
        uses: DeterminateSystems/nix-installer-action@main
      - name: activate devshell
        run: nix develop
      - name: build
        run: echo TODO && exit 1
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - name: check out repository
        uses: actions/checkout@v4
      - name: install Nix
        uses: DeterminateSystems/nix-installer-action@main
      - name: activate devshell
        run: nix develop
      - name: test
        run: echo TODO && exit 1
...
""",
    )


def dependabot() -> File:
    return File(
        name="dependabot.yaml",
        content="""---
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
...
""",
    )


def documentation_issue() -> File:
    return File(
        name="documentation_issue.yaml",
        content="""---
name: 📗 Documentation Issue
description: Report missing or incorrect documentation
labels: [documentation]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for submitting a documentation issue! It helps make `pxl` better.
  
  - type: dropdown
    attributes:
      label: What is the type of issue?
      multiple: true
      options:
        - Documentation is missing
        - Documentation is incorrect
        - Documentation is confusing
        - Example code is not working
        - Something else
  - type: textarea
    attributes:
      label: What is the issue?
    validations:
      required: true
  - type: textarea
    attributes:
      label: Where did you find it?
      description: If possible, please provide the URL(s) where you found this issue.
    validations:
      required: true
...
""",
    )


def envrc() -> File:
    return File(
        name=".envrc",
        content="""# .envrc is used by direnv (if installed) to automatically load the devshell
use flake . --impure
""",
    )


def feature_request() -> File:
    return File(
        name="feature_request.yaml",
        content="""---
name: 🚀 Feature Request
description: Suggest a feature, idea, or enhancement
labels: [feature]
body:
  - type: markdown
    attributes:
      value: |
        Thank you for submitting a feature request! It helps make `pxl` better.

  - type: textarea
    attributes:
      label: What problem would this feature solve?
    validations:
      required: true
  - type: textarea
    attributes:
      label: What solution are you proposing?
    validations:
      required: true
  - type: textarea
    attributes:
      label: What alternatives have you considered?
...
""",
    )


def flake(
    *,
    name: str,
    description: str,
    languages: set[Language] = set(),
    services: set[Service] = set(),
    extra_pkgs: set[str] = set(),
) -> File:
    default_languages = {Language.NIX, Language.SHELL}
    languages_str = "\n".join(
        f"                {line}"
        for language in languages | default_languages
        for line in str(language.value).splitlines()
    )
    services_str = "\n".join(
        f"                {line}"
        for service in services
        for line in str(service.value).splitlines()
    )
    pkgs_str = "\n".join(
        f"                {pkg}"
        for pkg in extra_pkgs
        | {
            pkg
            for option in (languages | default_languages | services)
            if isinstance(option.value, NixOption)
            for pkg in option.value.extra_pkgs()
        }
    )
    return File(
        name="flake.nix",
        content=f"""{{
  description = "{name} - {description}";

  inputs = {{
    devenv.url = "github:cachix/devenv";
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  }};

  outputs = {{
    self,
    devenv,
    flake-utils,
    nixpkgs,
    ...
  }} @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${{system}};
    in {{
      devShells = {{
        default = devenv.lib.mkShell {{
          inherit inputs pkgs;
          modules = [
            ({{
              pkgs,
              config,
              ...
            }}: {{
              enterShell = ''
                printf "\\033[0;1;36m\n{get_ascii_art(name)}DEVSHELL ACTIVATED\\033[0m\\n"
              '';
              languages = {{
{languages_str}
              }};
              packages = with pkgs; [
{pkgs_str}
              ];
              scripts = {{
              }};
              services = {{
{services_str}
              }};
            }})
          ];
        }};
      }};
      formatter = pkgs.alejandra;
      packages = {{
        devenv-up = self.devShells.${{system}}.default.config.procfileScript;
      }};
    }});
}}
""",
    )


def gitignore() -> File:
    return File(
        name=".gitignore",
        content=""".devenv/
.direnv/
__pycache__/
""",
    )


def issue_config() -> File:
    return File(
        name="config.yaml",
        content="""---
blank_issues_enabled: false
...
""",
    )


def license() -> File:
    return File(
        name="LICENSE",
        content=f"""MIT License

Copyright (c) {datetime.now().year} Generate

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    )


def pull_request() -> File:
    return File(
        name="PULL_REQUEST_TEMPLATE.md",
        content="""<!--
Before opening a pull request, please ensure you've done the following:

- 👷‍♀️ Created a small PR.
- 📝 Used a descriptive title.
- ✅ Provided tests for your changes (if applicable).
- 📗 Updated relevant documentation.

Please be patient! We will review your pull request as soon as possible.
-->

## Type
<!--
What type of change is this?
-->

- [ ] Bug Fix
- [ ] Documentation Update
- [ ] Feature
- [ ] Refactor

## Description
<!--
What does this change accomplish? Why did you make this change?
-->

## Testing
<!--
How did you test your changes?
-->

## Related Issues
<!--
For pull requests that close an issue, please include them below.
We follow [Github's guidance on linking issues to pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).
Example: "Closes #10"
-->
""",
    )


def readme(*, name: str, description: str) -> File:
    return File(
        name="README.md",
        content=f"""# {name}
{description}

## Usage


## Development
To initialize your development environment:
1. Install Nix by running the following command (one-time install)
   ```console
   curl -sL https://raw.githubusercontent.com/GenerateNU/init/main/scripts/install_nix.sh | sudo sh -s --
   ```
2. Navigate to the project root directory 
3. Activate the devshell by running the following command
   ```console
   nix develop --impure
   ```
> [!NOTE]
> Alternatively, [install direnv](https://direnv.net/docs/installation.html) to activate the devshell automatically

## Contributing
Developers can contribute to this project by writing and reviewing code.
When writing code:
- Don't push to the `main` branch. Instead, push to your own branch and open a pull request
- Open small pull requests
- Write useful tests, especially for essential or unique behavior
- All code must pass automated checks (formatters, linters, and tests) to be accepted
- At least one other developer must review and accept your pull request before merging
When reviewing code:
- Critique the code, not the developer
- Give actionable feedback
- Don't be afraid to express your opinions
- Don't make excessive nitpick comments (Ex: variable naming, position of code in a file, etc.)
""",
    )
