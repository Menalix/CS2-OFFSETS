import io
import json
from email.message import Message
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sync


class MirrorTests(unittest.TestCase):
    def run_mirror(self, data, root):
        response = io.BytesIO(json.dumps(data).encode())
        response.headers = Message()
        response.headers['Content-Type'] = 'application/json'
        response.headers['X-CS2-Build'] = '123'
        response.headers['X-CS2-Manifest'] = '456'
        with patch.object(sync, 'ROOT', root), patch.object(sync, 'urlopen', return_value=response):
            sync.main()

    def fixture(self):
        return {'offsets': {'client.dll': {'dwExample': 4096}},
                'client.dll': {'Example': {'field': 8}},
                'engine2.dll': {'Example': {'field': 16}},
                'buttons': {'client.dll': {'attack': 8192}},
                'interfaces': {'engine2.dll': {'Example001': 12288}},
                'worldrenderer.dll': {'Example': {'field': 32}}}

    def test_new_exports_keep_module_grouping(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            root = Path(directory)
            self.run_mirror(self.fixture(), root)
            for key in ('offsets', 'buttons', 'interfaces'):
                self.assertEqual(json.loads((root / (key + '.json')).read_text()), self.fixture()[key])
            self.assertEqual(json.loads((root / 'worldrenderer.dll.json').read_text()), {'worldrenderer.dll': self.fixture()['worldrenderer.dll']})
            metadata = json.loads((root / 'metadata.json').read_text())
            self.assertEqual((metadata['button_count'], metadata['interface_count']), (1, 1))

    def test_invalid_exports_leave_previous_files_intact(self):
        for kind in ('unknown', 'string', 'negative'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
                root = Path(directory)
                old = root / 'buttons.json'
                old.write_text('previous')
                data = self.fixture()
                if kind == 'unknown':
                    data['private'] = {'secret': 1}
                else:
                    data['buttons']['client.dll']['attack'] = '8192' if kind == 'string' else -1
                with self.assertRaises(ValueError):
                    self.run_mirror(data, root)
                self.assertEqual(old.read_text(), 'previous')


if __name__ == '__main__':
    unittest.main()
