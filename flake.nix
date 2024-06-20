{
  description = "init - Generating development environments";

  inputs = {
    devenv.url = "github:cachix/devenv";
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    devenv,
    flake-utils,
    nixpkgs,
    ...
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells = {
        default = devenv.lib.mkShell {
          inherit inputs pkgs;
          modules = [
            ({
              pkgs,
              config,
              ...
            }: {
              enterShell = ''
                printf "\033[0;1;36m
                   _      _ __
                  (_)__  (_) /_
                 / / _ \/ / __/
                /_/_//_/_/\__/

                DEVSHELL ACTIVATED\033[0m\n"
              '';
              languages = {
                python.enable = true;
                nix.enable = true;
                shell.enable = true;
              };
              packages = with pkgs; [
                bash
                black
                pyright
                commitizen
              ];
              scripts = {
              };
              services = {
              };
            })
          ];
        };
      };
      formatter = pkgs.alejandra;
      packages = {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
      };
    });
}
