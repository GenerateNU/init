{
  description = "init - Generate's base development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
      in
        with pkgs; {
          formatter = alejandra;
          devShells.default = mkShell {
            nativeBuildInputs = [
              just
              shellcheck
            ];

            shellHook = ''
              echo DEV SHELL ACTIVATED
            '';
          };
        }
    );
}
