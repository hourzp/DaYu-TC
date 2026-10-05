"""Pack the documented split ERA5 files into one physical 69-channel input."""
from pathlib import Path
from datetime import datetime
import argparse
import numpy as np

LEVELS=(50,100,150,200,250,300,400,500,600,700,850,925,1000)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',required=True,help='Contains YYYYMMDD and single/YYYYMMDD directories')
    p.add_argument('--time',required=True,help='UTC ISO time')
    p.add_argument('--output',required=True)
    a=p.parse_args();t=datetime.fromisoformat(a.time.replace('Z','+00:00'))
    if t.utcoffset() is not None and t.utcoffset().total_seconds()!=0:raise ValueError('Use UTC')
    if t.hour%6 or t.minute or t.second or t.microsecond:raise ValueError('Use a six-hour UTC timestamp')
    root=Path(a.root);day=t.strftime('%Y%m%d');stamp=t.strftime('%H_%M_%S')
    paths=[root/'single'/day/f'{stamp}-{v}.npy' for v in ('t2m','u10','v10','msl')]
    paths += [root/day/f'{stamp}-{v}-{level:.1f}.npy' for v in ('q','t','u','v','z') for level in LEVELS]
    array=np.empty((69,721,1440),dtype=np.float32)
    for i,path in enumerate(paths):
        x=np.load(path,allow_pickle=False).squeeze()
        if x.shape!=(721,1440) or not np.isfinite(x).all():raise ValueError(f'Invalid field: {path}')
        array[i]=x
    with Path(a.output).open('xb') as f:np.save(f,array,allow_pickle=False)
    print(a.output)

if __name__=='__main__':main()
