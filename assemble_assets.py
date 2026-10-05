"""Reassemble downloaded asset parts, checking each part before committing output."""
from pathlib import Path
import argparse
import hashlib
import json


def assemble(source, destination):
    source,destination=Path(source),Path(destination)
    index=json.loads((source/'download_index.json').read_text(encoding='utf-8'))
    if index.get('format')!=1:raise ValueError('Unsupported asset index')
    destination.mkdir(parents=True,exist_ok=True)
    for filename,parts in index['files'].items():
        if Path(filename).name!=filename or filename in ('.','..'):
            raise ValueError('Invalid destination name')
        final=destination/filename
        if final.exists():raise FileExistsError(final)
        temporary=destination/(filename+'.assembling')
        with temporary.open('xb') as out:
            for part in parts:
                name=part['name']
                if Path(name).name!=name or name in ('.','..'):raise ValueError('Invalid part name')
                digest=hashlib.sha256();size=0
                with (source/name).open('rb') as stream:
                    for chunk in iter(lambda:stream.read(8<<20),b''):
                        digest.update(chunk);size+=len(chunk);out.write(chunk)
                if size!=part['size'] or digest.hexdigest()!=part['sha256']:
                    raise ValueError(f'Corrupt part: {name}; incomplete .assembling file retained')
        temporary.rename(final)
        print('Assembled',filename)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--downloads',required=True);p.add_argument('--output',default='assets')
    a=p.parse_args();assemble(a.downloads,a.output)
