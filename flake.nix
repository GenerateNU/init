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
              printf "\033[0;1;36m
                 _      _ __ 
                (_)__  (_) /_
               / / _ \/ / __/
              /_/_//_/_/\__/ 

              DEVSHELL ACTIVATED\033[0m\n"
            '';
          };
        }
    );
}
