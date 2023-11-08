# artifact-shared

Shared kernel of artifact concepts, used by artifacts.

## How to declare it in your flake

Check the latest tag of the artifact repository: https://github.com/pythoneda-shared-artifact/artifact-shared-artifact/tags, and use it instead of the `[version]` placeholder below.

```nix
{
  description = "[..]";
  inputs = rec {
    [..]
    pythoneda-shared-artifact-artifact-shared = {
      [optional follows]
      url =
        "github:pythoneda-shared-artifact/artifact-shared-artifact/[version]?dir=artifact-shared";
    };
  };
  outputs = [..]
};
```

Should you use another PythonEDA modules, you might want to pin those also used by this project. The same applies to [https://nixos/nixpkgs](nixpkgs "nixpkgs") and [https://github.com/numtide/flake-utils](flake-utils "flake-utils").

The Nix flake is under the [https://github.com/pythoneda-shared-artifact/artifact-shared-artifact/tree/main/artifact-shared](artifact-shared "artifact-shared") folder of <https://github.com/pythoneda-shared-artifact/artifact-shared-artifact>.

