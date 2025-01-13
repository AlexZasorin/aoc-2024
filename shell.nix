{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = [
    pkgs.stdenv.cc.cc.lib
    pkgs.python312
    pkgs.poetry
    pkgs.nerd-fonts.jetbrains-mono
  ];

  shellHook = ''
    # Create local font directory if it doesn't exist
    mkdir -p ~/.local/share/fonts

    # Copy Fira Code fonts to local font directory
    cp -n ${pkgs.nerd-fonts.jetbrains-mono}/share/fonts/truetype/*.ttf ~/.local/share/fonts/

    # Update font cache
    if command -v fc-cache >/dev/null 2>&1; then
      fc-cache -f -v
    fi
  '';

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";
}
