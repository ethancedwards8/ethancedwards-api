{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { self, nixpkgs, ... }@inptus:
    let
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
    in
    {
      defaultPackage = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.python3Packages.buildPythonApplication rec {
          pname = "ethancedwards-quotes";
          version = "1.0";
          pyproject = true;

          src = ./.;

          build-system = with pkgs.python3Packages; [
              poetry-core
          ];

          dependencies = with pkgs.python3Packages; [
            flask-restful
            flask
            feedparser
            yt-dlp
            # add pygeocodio and podgen
          ];
        }
      );

      devShell = forAllSystems (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        pkgs.mkShell {
          buildInputs = with pkgs; [
            poetry
          ];
        }
      );
    };
}
