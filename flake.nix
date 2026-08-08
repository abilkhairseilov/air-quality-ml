{
  description = "Python dev environment for the air-quality-ml embedded sensors project";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
      pkgsFor = system: nixpkgs.legacyPackages.${system};
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = pkgsFor system;
          python = pkgs.python312;
          pythonPackages = python.withPackages (
            ps: with ps; [
              pyserial
              smbus2
              ipython
              pytest
            ]
          );
        in
        {
          default = pkgs.mkShellNoCC {
            packages = [
              pythonPackages
              pkgs.ruff
              pkgs.basedpyright
              pkgs.mypy
            ];
            shellHook = ''
              echo ""
              echo "  air-quality-ml dev shell"
              echo "  python:  $(python --version)"
              echo "  ruff:    $(ruff --version)"
              echo "  basedpyright: $(basedpyright --version)"
              echo "  mypy:    $(mypy --version)"
              echo "  pytest:  $(pytest --version | head -n1)"
              echo ""
            '';
          };
        }
      );

      formatter = forAllSystems (system: (pkgsFor system).ruff);
    };
}
