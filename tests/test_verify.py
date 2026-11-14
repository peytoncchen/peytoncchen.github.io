import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('site_verify', Path(__file__).resolve().parents[1] / 'scripts/verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class LocalReferences(unittest.TestCase):
    def test_relative_assets_and_root_fragments_then_missing_asset(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'support').mkdir()
            (root / 'asset.png').write_bytes(b'fixture')
            (root / 'index.html').write_text('<html lang="en"><title>Home</title><div id="app"></div><a href="/support/">Help</a><image-slot src="asset.png"></image-slot>')
            (root / 'support/index.html').write_text('<html lang="en"><title>Help</title><a href="/#app">App</a>')
            self.assertEqual(verify.verify(root), (2, []))
            (root / 'asset.png').unlink()
            self.assertTrue(any('missing local reference' in error for error in verify.verify(root)[1]))

    def test_generated_conditional_routes_require_rendered_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'index.html').write_text('<html lang="en"><title>Home</title><x-dc><sc-if><div id="image"></div></sc-if><sc-if><div id="image"></div></sc-if><a href="#route">App</a></x-dc>')
            self.assertEqual(verify.verify(root), (1, []))

    def test_missing_fragment_duplicate_ids_and_escape_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'index.html').write_text('<html lang="en"><title>Home</title><div id="a"></div><div id="a"></div><a href="#missing">Oops</a><img src="../escape.png">')
            errors = verify.verify(root)[1]
            for message in ('duplicate id', 'missing local fragment', 'escapes the site'):
                self.assertTrue(any(message in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
