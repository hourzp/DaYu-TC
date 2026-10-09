"""Download externally hosted tensor-only weights using a versioned SHA-256 manifest."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request


def checksum(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def download(entry, destination, base_url=None, *, _part=False):
    name, size, expected = entry['name'], entry['size'], entry['sha256']
    if name not in ('global_extreme.pt', 'global_normal.pt', 'region.pt') and not (
            _part and re.fullmatch(r'(global_extreme|global_normal|region)\.pt\.part[0-9]{4}', name)):
        raise ValueError('Unknown weight filename')
    if not isinstance(size, int) or size <= 0 or len(expected) != 64:
        raise ValueError('Invalid weight metadata')
    url = entry.get('url')
    if not url and base_url:
        url = base_url.rstrip('/') + '/' + urllib.parse.quote(name)
    if not url:
        raise ValueError('Weight URL is pending. Supply --base-url or add real per-file URLs to the manifest.')
    if urllib.parse.urlparse(url).scheme != 'https':
        raise ValueError('Weight downloads require HTTPS')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    final = destination / name
    if final.exists():
        if final.stat().st_size == size and checksum(final) == expected:
            print('Verified existing:', name); return
        raise ValueError(f'{final}: existing file does not match this release; refusing to overwrite')
    partial = destination / (name + '.part')
    offset = partial.stat().st_size if partial.exists() else 0
    if offset > size:
        raise ValueError(f'{partial}: partial file is too large; remove it before retrying')
    if offset < size:
        headers = {'User-Agent': 'DaYu-TC-weight-downloader'}
        if offset:
            headers['Range'] = f'bytes={offset}-'
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=60) as response:
            if urllib.parse.urlparse(response.geturl()).scheme != 'https':
                raise ValueError('Server redirected to a non-HTTPS URL')
            if response.status == 206:
                wanted = f'bytes {offset}-'
                if not response.headers.get('Content-Range', '').startswith(wanted):
                    raise ValueError('Unexpected server resume offset')
                mode = 'ab' if offset else 'wb'
            elif response.status == 200:
                offset, mode = 0, 'wb'
            else:
                raise ValueError(f'Unexpected response status: {response.status}')
            reported = offset
            with partial.open(mode) as stream:
                while True:
                    block = response.read(8 << 20)
                    if not block:
                        break
                    if offset + len(block) > size:
                        raise ValueError('Server returned more bytes than the manifest allows')
                    stream.write(block)
                    offset += len(block)
                    if offset - reported >= 100 << 20:
                        print(f'{name}: {offset / size:.0%}', flush=True)
                        reported = offset
    if partial.stat().st_size != size:
        raise ValueError(f'{partial}: download incomplete; rerun to resume')
    if checksum(partial) != expected:
        raise ValueError(f'{partial}: SHA-256 mismatch; retained for inspection, remove before retrying')
    partial.rename(final)
    print('Downloaded and verified:', name)


def download_weight(entry, destination, base_url=None):
    if not entry.get('parts'):
        return download(entry, destination, base_url)
    name = entry['name']
    if name not in ('global_extreme.pt', 'global_normal.pt', 'region.pt'):
        raise ValueError('Unknown weight filename')
    parts = entry['parts']
    if not parts or sum(p['size'] for p in parts) != entry['size']:
        raise ValueError('Multipart sizes do not match the complete weight')
    for number, part in enumerate(parts, 1):
        if part['name'] != f'{name}.part{number:04d}':
            raise ValueError('Multipart filenames must be ordered and belong to the selected model')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    final = destination / name
    if final.exists():
        if final.stat().st_size == entry['size'] and checksum(final) == entry['sha256']:
            print('Verified existing:', name); return
        raise ValueError(f'{final}: existing file does not match this release; refusing to overwrite')
    directory = destination / '.weight_parts'
    for part in parts:
        download(part, directory, base_url, _part=True)
    temporary = destination / (name + '.assembling')
    digest = hashlib.sha256()
    size = 0
    with temporary.open('wb') as output:
        for part in parts:
            with (directory / part['name']).open('rb') as source:
                while block := source.read(8 << 20):
                    output.write(block); digest.update(block); size += len(block)
    if size != entry['size'] or digest.hexdigest() != entry['sha256']:
        raise ValueError('Assembled weight SHA-256/size mismatch; incomplete output retained for inspection')
    temporary.rename(final)
    print('Assembled and verified:', name)


def main():
    parser = argparse.ArgumentParser(description='Download external DaYu-TC weights; no weights are bundled with GitHub')
    parser.add_argument('--manifest', default=str(Path(__file__).with_name('weights_manifest.json')))
    parser.add_argument('--output', default='assets')
    parser.add_argument('--base-url', help='HTTPS directory containing the three exact filenames')
    parser.add_argument('--model', choices=['all', 'global_extreme', 'global_normal', 'region'], default='all')
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    entries = [e for e in manifest['files'] if args.model == 'all' or e['name'] == args.model + '.pt']
    if not entries:
        parser.error('Selected model is absent from the manifest')
    try:
        for entry in entries:
            download_weight(entry, args.output, args.base_url or manifest.get('download_url'))
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Weight download stopped: {exc}\n')


if __name__ == '__main__':
    main()
