{
  description = "Ethan's Api Dev Flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs@{ self, nixpkgs, ... }:
  let
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
  in
    {
      devShell = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };

          pythonEnvironment = pkgs.python312.withPackages (ps: with ps; [
            flask
            flask-restful
            yt-dlp
            podgen
            feedparser
            pygeocodio
            jobspy
          ]);
        in
        with pkgs;
        mkShell {
          name = "dev shell";

          # tbh idrk what the move is here but nix-ld fixes my issues with uv
          nativeBuildInputs = [
            uv # pythonEnvironment
          ];
        }
      );
    };
}
