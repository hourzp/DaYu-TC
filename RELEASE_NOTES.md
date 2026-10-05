# v0.1.0-rc.1 — pretrained inference release candidate

This prerelease provides the DaYu-TC inference entry point, architecture pseudocode,
three tensor-only weight sets, static inputs, normalization statistics and a native
Windows x86_64 / CPython 3.12 runtime wheel. The model implementation is compiled;
training code and the original training pipeline are omitted.

## Download and install

Download the wheel, `download_index.json` and all 19 `*.part*` files from this release.
Read `windows_VALIDATION.json` for the exact tested environment and limitations.
Use `assemble_assets.py` to reconstruct the asset directory, then follow README.md.
The asset parts total approximately 8.7 GB; allow another 8.7 GB for reconstruction.

## Verified

- Installed native global/regional small-model forwards match the original implementation bitwise on CPU.
- All three full pretrained state dictionaries load strictly.
- Asset SHA-256 checks, time encoding and regional remapping pass.
- The wheel contains four native extensions and no model implementation source or Python bytecode.

## Limitations

- Full-resolution NVIDIA/DCU forecasts and production memory requirements have not been validated.
- Linux/DCU binaries are not included; the current wheel only supports Windows/Python 3.12.
- The `global_normal` filename does not imply a disabled-adapter baseline; its saved mode is `extreme`.
- The CLI provides six-hour steps; repeated product-grid resizing differs from a native-grid multistep evaluation.
- No original training reproduction is provided. No open-source license has been assigned.

This is a prerelease for inspection and inference integration, not a claim of completed accelerator qualification.
