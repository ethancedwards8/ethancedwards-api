{
  description = "a flake for flask based api for quotes";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-compat = { url = "github:edolstra/flake-compat"; flake = false; };
  };

  outputs = { self, nixpkgs, flake-compat, ... }@inputs:
    let
      supportedSystems = [ "x86_64-linux" "i686-linux" "aarch64-linux" "x86_64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs supportedSystems (system: f system);
    in
      {
        defaultPackage = forAllSystems (system:
          let
            pkgs = import nixpkgs { inherit system; };
          in
            pkgs.python3Packages.buildPythonApplication rec {
              pname = "ethancedwards-quotes";
              version = "1.0";
              src = ./.;

              propagatedBuildInputs = with pkgs.python3Packages; [ flask flask-restful ];
            }
        );

        devShell = forAllSystems (system:
          let
            pkgs = import nixpkgs { inherit system; };
          in
            pkgs.mkShell {
              nativeBuildInputs = with pkgs.python3Packages; [
                flask
                flask-restful
                setuptools
              ];

              BuildInputs = with pkgs.python3Packages; [
                flask
                flask-restful
                feedparser
                setuptools
              ];
            }
        );
      };
}
