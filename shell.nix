{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = [
    pkgs.stdenv.cc.cc.lib
    pkgs.python312
    pkgs.poetry
  ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";
}
