"""Mirror only Hexui's public JSON API; no credentials or game binaries required."""
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    'client.dll', 'engine2.dll', 'inputsystem.dll', 'matchmaking.dll',
    'soundsystem.dll', 'animationsystem.dll', 'host.dll', 'materialsystem2.dll',
    'networksystem.dll', 'panorama.dll', 'particles.dll', 'pulse_system.dll',
    'rendersystemdx11.dll', 'resourcesystem.dll', 'scenesystem.dll',
    'schemasystem.dll', 'server.dll', 'steamaudio.dll', 'vphysics2.dll', 'worldrenderer.dll', 'buttons', 'interfaces', 'offsets',
}


def validate(node, depth=0):
    if not isinstance(node, dict) or depth > 3 or len(node) > 10000:
        raise ValueError('Invalid public dump structure')
    for key, value in node.items():
        if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.:]{0,255}', key):
            raise ValueError('Invalid public symbol')
        if isinstance(value, dict):
            validate(value, depth + 1)
        elif type(value) is not int or not 0 <= value <= 2147483647:
            raise ValueError('Invalid public offset')


def main():
    request = Request('https://hexui.com/offsets/api/', headers={
        'Accept': 'application/json', 'User-Agent': 'Hexui-CS2-Offsets-Mirror/1.0'})
    with urlopen(request, timeout=60) as response:
        if response.headers.get_content_type() != 'application/json':
            raise ValueError('Expected JSON response')
        raw = response.read(4194305)
        build = response.headers.get('X-CS2-Build', '')
        manifest = response.headers.get('X-CS2-Manifest', '')
    if len(raw) > 4194304 or not re.fullmatch(r'[0-9]{1,20}', build) or not re.fullmatch(r'[0-9]{1,20}', manifest):
        raise ValueError('Invalid dump size or build identity')
    data = json.loads(raw)
    validate(data)
    if not {'offsets', 'client.dll', 'engine2.dll'} <= data.keys() or not data.keys() <= MODULES:
        raise ValueError('Unexpected public modules')
    if not all(data[key] for key in ('offsets', 'client.dll', 'engine2.dll')):
        raise ValueError('Required public data missing')
    # Validate the entire response before touching the previously mirrored dump.
    exports = {key + '.json': value if key in {'offsets', 'buttons', 'interfaces'} else {key: value}
               for key, value in data.items()}
    exports['metadata.json'] = {'source': 'https://hexui.com/offsets/',
                                'build_id': build, 'manifest': manifest,
                                'button_count': sum(len(rows) for rows in data.get('buttons', {}).values()),
                                'interface_count': sum(len(rows) for rows in data.get('interfaces', {}).values())}
    for name, value in exports.items():
        (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    for key in MODULES - data.keys():
        (ROOT / (key + '.json')).unlink(missing_ok=True)
    print(f'Mirrored {len(data)} public exports for CS2 build {build}')


if __name__ == '__main__':
    main()
