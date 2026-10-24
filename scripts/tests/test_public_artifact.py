from pathlib import Path
import hashlib
import json
import tempfile
import unittest

from scripts.build_public_artifact import build


class PublicArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / "public-docs").mkdir()
        (self.root / "public-docs/index.html").write_text("<h1>Public</h1>")
        self.manifest = {"schema_version": 1, "files": [
            {"source": "public-docs/index.html", "destination": "index.html"}]}
        self.write_manifest()

    def write_manifest(self):
        (self.root / "docs/public-artifact.json").write_text(json.dumps(self.manifest))

    def test_only_allowlisted_content_and_hashes_are_exported(self):
        (self.root / ".env").write_text("must not escape")
        (self.root / "public-docs/not-approved.html").write_text("not approved")
        first, second = self.root / "first", self.root / "second"
        result = build(self.root, first)
        build(self.root, second)
        self.assertEqual(sorted(p.name for p in first.iterdir()), ["artifact-manifest.json", "index.html"])
        self.assertEqual(result["files"][0]["sha256"], hashlib.sha256((first / "index.html").read_bytes()).hexdigest())
        for path in first.iterdir():
            self.assertEqual(path.read_bytes(), (second / path.name).read_bytes())

    def test_symlink_cannot_smuggle_unapproved_content(self):
        source = self.root / "public-docs/index.html"
        source.unlink()
        private = self.root / "private.html"
        private.write_text("private")
        source.symlink_to(private)
        with self.assertRaises(ValueError):
            build(self.root, self.root / "output")
        self.assertFalse((self.root / "output").exists())

    def test_paths_cannot_escape_public_boundary(self):
        for source, destination in [("README.md", "index.html"),
                                    ("public-docs/../private.html", "index.html"),
                                    ("public-docs/index.html", "../index.html"),
                                    ("public-docs/index.html", "/index.html")]:
            with self.subTest(source=source, destination=destination):
                self.manifest["files"] = [{"source": source, "destination": destination}]
                self.write_manifest()
                with self.assertRaises(ValueError):
                    build(self.root, self.root / "output")

    def test_existing_directory_is_never_deleted_or_merged(self):
        output = self.root / "output"
        output.mkdir()
        (output / "keep.html").write_text("preserve")
        with self.assertRaises(ValueError):
            build(self.root, output)
        self.assertEqual((output / "keep.html").read_text(), "preserve")

    def test_duplicate_and_reserved_destinations_rejected(self):
        for destination in ["index.html", "artifact-manifest.json"]:
            self.manifest["files"].append({"source": "public-docs/index.html", "destination": destination})
            self.write_manifest()
            with self.assertRaises(ValueError):
                build(self.root, self.root / "output")
            self.manifest["files"].pop()


if __name__ == "__main__":
    unittest.main()
