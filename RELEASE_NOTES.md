# v0.1.0-rc.1 — inference software release candidate

This prerelease provides inference entry-point code, architecture pseudocode,
static inputs, normalization statistics and a Windows x86_64 / CPython 3.12 native
runtime. The neural implementation is compiled. Training code is not included.

**Weights are not included in GitHub. Their external download location will be added later.**
Until then, this release supports installation checks but does not by itself supply
all files required for pretrained inference.

## Attachments

- `dayu_tc_runtime-0.1.0-cp312-cp312-win_amd64.whl`: native runtime.
- `inference_support.zip`: inference configurations, static fields, normalization
  statistics and a complete-asset SHA-256 manifest, extracted under `assets/`.
- `weights_manifest.json`: expected external weight filenames, sizes and SHA-256 values.
- `windows_VALIDATION.json`: exact local test environment and results.

## Verified locally

- Installed binary small-model forwards match the original implementation bitwise on CPU.
- All three full pretrained state dictionaries load strictly using local developer weights.
- Asset checksums, time encoding and regional remapping pass.
- The wheel contains four native extensions, without model source or Python bytecode.

## Limitations

- An external weight download link is not yet published.
- Full-resolution NVIDIA/DCU inference and production memory requirements are unverified.
- Linux/DCU binaries are not included; this wheel is for Windows/Python 3.12 only.
- The global_normal checkpoint also selects extreme mode; its name is not proof of a baseline.
- Repeated CLI product-grid resizing differs from native-grid multistep evaluation.
- The original training pipeline is omitted, and no open-source license has been assigned.
