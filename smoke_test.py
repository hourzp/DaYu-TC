"""CPU installation check with small random models; not a forecast-quality test."""
import torch
from dayu_tc_runtime.factory import build_global, build_region


def main():
    torch.set_num_threads(2)
    torch.manual_seed(2026)
    cfg = {
        'inference_mode': 'joint',
        'data': {'static_names': ['sin_lat','cos_lat','sin_lon','cos_lon','land_sea_mask']},
        'model': {
            'image_size': [32,40], 'window_size': 2, 'patch_size': 2,
            'down_times': 1, 'embed_dim': 64, 'num_heads': 4, 'depths': [1,1],
            'mlp_ratio': 2, 'activation_checkpointing': False, 'residual_reference': 'driver',
            'dual_branch': {'surface_channels': 4, 'surface_embed_dim': 32, 'upper_embed_dim': 32},
            'adapters': {'local_hidden_dim': 32,'axial_dim': 32,'axial_heads': 4,
                         'axial_kv_reduction': 2,'axial_after_stage': 0,'aux_hidden_dim': 32},
        },
    }
    history = torch.randn(1,2,69,32,40)
    driver = torch.randn(1,69,32,40)
    static = torch.randn(1,5,32,40)
    time = torch.randn(1,12)
    for name, builder in [('global',build_global), ('region',build_region)]:
        model = builder(cfg).eval().requires_grad_(False)
        with torch.inference_mode():
            result = model(history,driver,time,static) if name=='region' else model(history,time,static)
        if tuple(result.shape)!=(1,69,32,40) or not torch.isfinite(result).all():
            raise RuntimeError(f'{name}: invalid forward output')
        print(f'{name}: binary forward passed')
    print('Random small-model installation check only; full pretrained inference requires release assets and target hardware.')


if __name__=='__main__':main()
