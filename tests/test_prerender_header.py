"""Publication keeps every responsive and reduced-motion source usable."""

from hashlib import sha256
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import prerender_header


class PrerenderPublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "assets").mkdir()
        self.output = self.root / "output"
        self.output.mkdir()
        self.manifest = {}
        lines = []
        for variant in prerender_header.VARIANTS:
            # A container signature suffices for the copy/integrity contract;
            # real decoding and animation are verified in Chromium and Firefox.
            data = b"RIFF\x10\x00\x00\x00WEBP" + variant.encode()
            filename = f"header-{variant}.webp"
            (self.output / filename).write_bytes(data)
            self.manifest[variant] = {"file": filename, "bytes": len(data),
                                      "sha256": sha256(data).hexdigest()}
            lines.extend((f'assets/header-{variant}-0123456789ab.svg',
                          f'assets/header-{variant}-still-0123456789ab.svg'))
        self.before = "\n".join(lines)
        (self.root / "README.md").write_text(self.before)

    def test_partial_build_leaves_readme_and_assets_untouched(self):
        del self.manifest["mobile-light"]
        with patch.object(prerender_header, "ROOT", self.root):
            with self.assertRaises(ValueError):
                prerender_header.publish(self.manifest, self.output)
        self.assertEqual((self.root / "README.md").read_text(), self.before)
        self.assertEqual(list((self.root / "assets").iterdir()), [])

    def test_corrupted_last_variant_cannot_partially_publish(self):
        (self.output / "header-mobile-light.webp").write_bytes(b"changed")
        with patch.object(prerender_header, "ROOT", self.root):
            with self.assertRaises(ValueError):
                prerender_header.publish(self.manifest, self.output)
        self.assertEqual((self.root / "README.md").read_text(), self.before)
        self.assertEqual(list((self.root / "assets").iterdir()), [])

    def test_complete_build_keeps_svg_motion_fallbacks_and_is_idempotent(self):
        with patch.object(prerender_header, "ROOT", self.root):
            prerender_header.publish(self.manifest, self.output)
            published = (self.root / "README.md").read_text()
            prerender_header.publish(self.manifest, self.output)
        self.assertEqual((self.root / "README.md").read_text(), published)
        for variant, metadata in self.manifest.items():
            self.assertIn(f'header-{variant}-{metadata["sha256"][:12]}.webp', published)
            self.assertIn(f'header-{variant}-still-0123456789ab.svg', published)
        self.assertEqual(len(list((self.root / "assets").glob("*.webp"))), 4)


if __name__ == "__main__":
    unittest.main()
