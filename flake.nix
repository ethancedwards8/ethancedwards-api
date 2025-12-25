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
        in
        with pkgs;
        mkShell {
          name = "dev shell";

          nativeBuildInputs = [ uv ];

          build-system = with python3Packages; [
              hatchling
          ];

          dependencies = with python312Packages; [
              flask
              flask-restful
              yt-dlp
              podgen
              feedparser
              pygeocodio
              jobspy
          ];
        }
      );
    };
}
