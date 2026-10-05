# DaYu-TC inference release

**Release candidate — full-resolution accelerator acceptance is pending.**
The current release supports installation and CPU checks on Windows x86_64 / Python 3.12.
Full-resolution accelerator forecasts have not yet been validated.

Download the binary runtime, inference support data and validation report from the
[v0.1.0-rc.1 release](https://github.com/hourzp/DaYu-TC/releases/tag/v0.1.0-rc.1).
**Weights are hosted separately. Their download location is pending; see [WEIGHTS.md](WEIGHTS.md).**

This repository provides public inference entry-point code, architecture pseudocode,
and instructions for external tensor-only weights and binary model runtimes. The neural model
implementation is distributed as compiled extensions, not open Python model source.
Training code and the original training pipeline are not provided.

## Install

An initial Windows x86_64 / CPython 3.12 native runtime wheel has been built.
Its CPU validation is documented separately; full-resolution NVIDIA validation and
Linux/DCU builds are pending. Use compatible CUDA-enabled PyTorch for NVIDIA inference.
Install the runtime wheel built for the same OS, CPU architecture and Python ABI:

```bash
python -m pip install ./dayu_tc_runtime-<version>-<matching-platform>.whl
python infer.py doctor
python smoke_test.py
```

The native wheel, support data and validation report are distributed with the tagged
prerelease. Installation of PyTorch is environment-specific; install
it first using the supported NVIDIA/PyTorch combination. The runtime wheel must not
replace a vendor accelerator build with an unrelated PyTorch installation.

The available Windows wheel is named
`dayu_tc_runtime-0.1.0-cp312-cp312-win_amd64.whl`. It contains four native extensions
and an empty package initializer, with no Python implementation or bytecode files.
It must not be installed on Linux or under a different Python ABI.

With GitHub CLI, download the runtime and support files using:

```bash
gh release download v0.1.0-rc.1 --repo hourzp/DaYu-TC --dir downloads
python -m zipfile -e downloads/inference_support.zip .
```
Then place the three externally obtained `.pt` files into `assets/`, following
[WEIGHTS.md](WEIGHTS.md), and run `python infer.py verify --assets assets`.
Until the external download link is supplied, users can run the small random-model
installation check but cannot run pretrained inference from this repository alone.
`assemble_assets.py` is an optional utility for externally distributed multipart
assets; the current GitHub release does not contain weight parts.

## Inputs and outputs

Each input is a NumPy float32 array `[69,721,1440]` in physical units, no pickle.
Channels: `2T,10U,10V,MSL`, then `Q,T,U,V,Z`, each at levels
`50,100,150,200,250,300,400,500,600,700,850,925,1000 hPa`.
Units: K, m/s, m/s, Pa; Q kg/kg, T K, U/V m/s, Z m²/s².
Latitude decreases north to south; global longitude increases from 0° eastward.
Regional grid coordinates follow ARCHITECTURE.md's mapping (not arbitrary crops).
The runtime validates shape, dtype and finiteness; the caller is responsible for
correct channel order, units, coordinates and timestamp provenance.

`--previous` is t-6h; `--current` is t; `--time` is t in UTC at 00/06/12/18.
The regional driver is a global *forecast* valid at t+6h, already remapped to the
regional grid. It must not be replaced with future analysis data.

For the split-file ERA5 convention, use:

```bash
python pack_era5.py --root /path/to/era5 --time 2023-07-22T06:00:00 --output global_t.npy
```
No observational input dataset is redistributed in this code repository.

```bash
python infer.py predict --assets assets --model global_extreme \
  --previous global_tminus6.npy --current global_t.npy --time 2023-07-22T06:00:00 \
  --output global_tplus6.npy --regional-driver-output driver_tplus6.npy

python infer.py predict --assets assets --model region \
  --previous region_tminus6.npy --current region_t.npy --driver driver_tplus6.npy \
  --time 2023-07-22T06:00:00 --output region_tplus6.npy
```

Run global and regional processes sequentially to release GPU model memory between
steps. Outputs are physical float32 `[69,721,1440]`. Existing outputs are not overwritten.
Default precision is FP32; no performance or memory claims are made before validation.
`--device cpu` is available for diagnostics; full models may be prohibitively slow.

For autoregressive forecasts, roll both global and regional histories forward and
generate each driver from the same global initialization and matching forecast lead.
The CLI performs one six-hour step per invocation. Reusing its restored 721-row
products introduces another resize at every step; this is not a bitwise reproduction
of an evaluation pipeline that retains 720-row normalized states in memory. A
native-grid multi-step acceptance test is required before reproducing long-lead tables.

## Release assets

`inference_support.zip` supplies inference-only `.json` configurations, `_static.npy`,
`_stats.npz`, and `manifest.json` SHA-256 checksums under `assets/`.
`global_extreme.pt`, `global_normal.pt`, and `region.pt` tensor state dictionaries
are distributed externally, with their download location pending.
Use `global_extreme` for the documented nested
pipeline; `global_normal` preserves the supplied filename but its checkpoint also
selects the `extreme` inference mode. Do not interpret that filename as proof of a
disabled-adapter baseline; the checkpoint configuration is authoritative.
Model availability and inference reproducibility require the runtime, support data
and external weights. Weight filenames and checksums are in `weights_manifest.json`
in the release assets.

## Availability scope

This repository publishes inference entry-point code, architecture pseudocode,
support data and a Windows/Python 3.12 binary runtime. The neural network implementation
is provided in compiled form. Training code and the original training pipeline are
not included. The external weight download location has not yet been published.
Do not claim that pretrained weights are publicly available until that link is live.

Do not substitute “fully open-source model code” for this statement. A pseudocode
description plus a binary runtime is not publication of the model implementation source.

## License and citation

An explicit redistribution or open-source license has not yet been assigned to the
code, binary runtime or weights. This repository does not claim an open-source license.
Author and paper citation metadata will be added when available. No observational
input dataset is included. Contact the repository maintainer about licensing.
