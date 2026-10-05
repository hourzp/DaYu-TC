# DaYu-TC architecture pseudocode

This is descriptive pseudocode, not executable model source. Exact inference
operators are distributed in the platform-specific binary runtime. Model dimensions
and static-channel order accompany the released tensor weights.

```text
GLOBAL_STEP(global[t-6h], global[t], time):
    x = normalize(resize(history, 720 x 1440))
    tokens = fuse(surface_static_patch_embedding(x), upper_air_patch_embedding(x))
    tokens += trend_gate * trend_adapter(x[t] - x[t-6h])  # active variant only
    low, skip = downsample(tokens, time_encoding(time))
    detail = local_detail(tokens, low)                  # active variant only
    features = window_attention_stages(low)
    inject gated compressed axial attention at the configured stage
    decoded = upsample(fuse_stage_features(features), skip, time_encoding(time))
    decoded += local_gate * restore(detail)             # active variant only
    forecast = x[t] + patch_reconstruction(decoded)
    return restore_grid(denormalize(forecast), 721 x 1440)

REGION_STEP(region[t-6h], region[t], global_driver[t+6h], time):
    normalize and resize all dynamic fields
    combine the two regional history frames and target-time global driver
    embed surface/static and upper-air channels separately, then fuse
    derive trend from regional history only
    run regional encoder, window/axial processor, decoder and local-detail path
    use nonperiodic regional convolution boundaries
    baseline = global_driver[t+6h] if released residual_reference == "driver"
               else region[t]
    forecast = baseline + reconstructed_delta
    return restore_grid(denormalize(forecast), 721 x 1440)
```

Global-to-regional mapping follows bilinear resize to 2001 x 4000 with
`align_corners=True`, then rows `[391:1112]`, columns `[833:2273]`.
This mapping acts directly on the 720-row normalized global prediction, followed
by denormalization; do not first restore the global product to 721 rows.
The runtime computes the same sampling coordinates without constructing the
entire intermediate field. Normalization-grid resizing uses `align_corners=False`.
The time embedding uses the original implementation's day-of-year/366 and hour/24
sin/cos values for t-6h, t and t+6h, without introducing an additional 2π factor.

This release omits optimization, losses, training data processing and sampling,
training schedules, and training-resume state. Weights and architecture information
do not technically prevent independent fine-tuning or independently designed training.
