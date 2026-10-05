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
