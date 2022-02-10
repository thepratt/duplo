let
  pinned =
    import (builtins.fetchTarball {
      name = "nixos-20.09";
      url = https://github.com/NixOS/nixpkgs/archive/20.09.tar.gz;
      sha256 = "1wg61h4gndm3vcprdcg7rc4s1v3jkm5xd7lw8r2f67w502y94gcy";
    }) {};

  systemBuildInputs = (
    with pinned;
    {
      x86_64-linux = [
        inotify-tools
      ];
      x86_64-darwin = [
        darwin.apple_sdk.frameworks.CoreFoundation
        darwin.apple_sdk.frameworks.CoreServices
      ];
    }
  );

in
  with pinned;

  mkShell {
    buildInputs = [
      poetry
      python39
    ] ++ systemBuildInputs.${system};
    preConfigure = ''
      export LANG=en_US.UTF-8
    '';
    shellHook = ''
      export LC_ALL=C.UTF-8
    '';
  }
