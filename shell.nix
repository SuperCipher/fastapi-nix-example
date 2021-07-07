{ pkgs ? import <nixpkgs> {} }:

with pkgs.python3Packages;

pkgs.mkShell {
  name = "python${python.pythonVersion}-environment";
  strictDeps = true;
  nativeBuildInputs = [ pkgs.curl uvicorn pytest ];
  /* buildInputs = [ aiosqlite databases fastapi sqlalchemy pytest-asyncio mock ]; */
  buildInputs = [ aiosqlite databases sqlalchemy pytest-asyncio mock];

  shellHook = ''
    prefix=$PWD/inst
    export PATH=$prefix/bin:$PATH
    export PYTHONPATH=$prefix/lib/python${python.pythonVersion}/site-packages:$PYTHONPATH

    mkdir -p $prefix/lib/python${python.pythonVersion}/site-packages
  '';
}


/* with import <nixpkgs> {};
let
  pythonEnv = python38.withPackages (ps: [
    ps.numpy
    ps.toolz
    ps.virtualenv
  ]);
in mkShell {
  packages = [
    pythonEnv

    black
    mypy

    libffi
    openssl
  ];
} */
