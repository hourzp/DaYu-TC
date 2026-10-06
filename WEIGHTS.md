# External pretrained weights

**Download location: pending.** The maintainer will add the external hosting link here.
Weights are intentionally not uploaded to the Git repository or GitHub Release.

| File | Role |
|---|---|
| `global_extreme.pt` | Global forecast model used by the documented nested pipeline |
| `global_normal.pt` | Additional supplied global checkpoint; its saved inference mode is also `extreme` |
| `region.pt` | Regional nested model with the global forecast as residual reference |

These are tensor-only state dictionaries, without optimizer, scheduler, RNG state
or original training configuration. Expected byte sizes and SHA-256 values are
published in the release's `weights_manifest.json`.

When the external weights become available:

1. Download and extract `inference_support.zip` from the GitHub release.
2. Download the three weight files from the external location specified above.
3. Place them alongside the support files under `assets/`.
4. Run `python infer.py verify --assets assets` before pretrained inference.

The complete pretrained inference bundle requires roughly 8.7 GB of local storage.
The CPU random-model smoke test can run without these weights and is not a forecast-quality test.

## Linked downloads

`weights_manifest.json` in this repository fixes the weight filenames, byte sizes,
SHA-256 values and compatible inference release. Its URLs are deliberately empty
until real external hosting is published.

After the maintainer fills in the per-file URLs, users can run:

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
model repository can provide a download mirror with a fixed revision. Hosting and
DOI registration have not been performed by this repository.
