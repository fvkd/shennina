{
  description = "Shennina development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      nixpkgsFor = forAllSystems (system: import nixpkgs { inherit system; config.allowUnfree = true; });
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgsFor.${system};
          pythonEnv = pkgs.python3.withPackages (ps: with ps; [
            pip
            virtualenv
            requests
            flask
            termcolor
            tensorflow
            pandas
            matplotlib
            numpy
            numpydoc
            pymetasploit3
            python-nmap
          ]);
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              pythonEnv
              nmap
              metasploit
              gcc
              zlib
              libffi
            ];

            shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc pkgs.zlib ]}
              echo "Welcome to Shennina dev shell (NixOS Unstable)"
              echo "Python environment is pre-loaded with dependencies."
              echo "Note: If you need to install more packages, use 'pip install --user' or add them to flake.nix"
            '';
          };
        }
      );
    };
}
