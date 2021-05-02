with import <nixpkgs> {};

python3Packages.buildPythonApplication rec {
  pname = "ethancedwards-quotes";
  version = "1.0";
  src = ./.;

  propagatedBuildInputs = with python3Packages; [ flask flask-restful ];
}
