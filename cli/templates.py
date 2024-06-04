MIT_LICENSE = """
MIT License

Copyright (c) 2024 Generate

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
"""

PULL_REQUEST_TEMPLATE = """
# Description

[Link to Ticket](insert the link to your ticket here)

Please include a summary of the changes and the related issue. Please also include relevant motivation and context.

# How Has This Been Tested?

Please describe the tests that you ran to verify your changes.
If they are unit tests, provide the file name the tests are in.
If they are not unit tests, describe how you tested the change.

# Checklist

- [ ] I have performed a self-review of my code
- [ ] I have reached out to another developer to review my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] New and existing unit tests pass locally with my changes
"""

def get_flake(pkgs: list[str]) -> str:
    pkgs_str = "\n".join(f"\t\t\t\t\t\t\t{pkg}" for pkg in pkgs)
    return f"""
{{
    description = "init - Generate's base development environment";

    inputs = {{
        nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
        flake-utils.url = "github:numtide/flake-utils";
    }};

    outputs = {{
        self,
        nixpkgs,
        flake-utils,
    }} @ inputs:
        flake-utils.lib.eachDefaultSystem (
            system: let
                pkgs = import nixpkgs {{inherit system;}};
            in
                with pkgs; {{
                    formatter = alejandra;
                    devShells.default = mkShell {{
                        nativeBuildInputs = [
                            just
                            shellcheck
{pkgs_str}
                        ];

                        shellHook = ''
                            echo DEV SHELL ACTIVATED
                        '';
                    }};
                }}
        );
}}
"""
