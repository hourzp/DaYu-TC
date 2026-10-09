# External pretrained weights

**Download location:** [10.5281/zenodo.23181947](https://zenodo.org/records/23181947). Compatible inference release: v0.1.0-rc.1.
Weights are intentionally not uploaded to the Git repository or GitHub Release.

| File | Role |
|---|---|
| `global_extreme.pt` | Global forecast model used by the documented nested pipeline |
| `global_normal.pt` | Additional supplied global checkpoint; its saved inference mode is also `extreme` |
| `region.pt` | Regional nested model with the global forecast as residual reference |

These are tensor-only state dictionaries, without optimizer, scheduler, RNG state
or original training configuration. Expected byte sizes and SHA-256 values are
published in the release's `weights_manifest.json`.

To use the published weights:

1. Download and extract `inference_support.zip` from the GitHub release.
2. Run `python download_weights.py --output assets` from the latest repository checkout.
3. The downloader obtains the 128 MiB parts, resumes interrupted downloads, and verifies both parts and assembled complete weights.
4. Run `python infer.py verify --assets assets` before pretrained inference.

The record stores 66 binary weight parts plus support files. The original three `.pt` weights are reconstructed without changing their bytes. Keep at least 18 GB of free disk space for downloaded parts and assembled weights.

The complete pretrained inference bundle requires roughly 8.7 GB of local storage.
The CPU random-model smoke test can run without these weights and is not a forecast-quality test.

## Linked downloads

`weights_manifest.json` in this repository fixes the weight filenames, byte sizes,
SHA-256 values and compatible inference release. Its URLs are fixed
and point to the published Zenodo record.

Download and verify the published weights with:

```bash
python download_weights.py --output assets
python infer.py verify --assets assets
```

Alternatively, `--base-url` accepts an HTTPS directory containing the exact three
filenames. For Hugging Face, pin a full commit revision in the resolve URL; for
Zenodo, use the file URLs of a specific published record. Do not silently replace
weights under an existing version. The downloader resumes partial files when the
server supports HTTP Range, verifies SHA-256 before committing a file, and refuses
to overwrite a conflicting existing weight.

Recommended research release layout: GitHub for inference software; a separately
published Zenodo record for pretrained weights and a citable DOI. A Hugging Face
model repository can provide a download mirror with a fixed revision. The weight record is now published with DOI 10.5281/zenodo.23181947. GitHub automatic software archival is a separate account setting.

## Weight license

The Zenodo weight record is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Attribution is required; commercial use requires separate authorization. This does not assign a license to the GitHub software or compiled runtime.
