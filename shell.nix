{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  name = "air-quality-ml";

  packages = [
    (pkgs.python313.withPackages (ps: with ps; [
      # Data preparation, CPU model training, and model persistence.
      numpy
      pandas
      scipy
      scikit-learn
      joblib

      # Exploration and the existing visualization script.
      matplotlib
      seaborn
      jupyterlab
      ipykernel
      ipywidgets

      # Sensor collection.
      pyserial
      smbus2
    ]))
    pkgs.ruff
  ];

  # Keep user-installed Python packages out of the Nix environment.
  PYTHONNOUSERSITE = "1";

  # shellHook = ''
  #   # Leave non-interactive commands such as nix-shell --run alone.
  #   if [[ $- == *i* ]]; then
  #     export SHELL=${pkgs.zsh}/bin/zsh
  #     exec "$SHELL" -i
  #   fi
  # '';
}
