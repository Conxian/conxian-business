"""Real offline archive intake checks; no mocked Kubo or success receipts."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.build_public_artifact import ROOT
from scripts.export_public_ipfs import export
from scripts.verify_public_ipfs_release import verify


@unittest.skipUnless(os.environ.get("CONXIAN_KUBO_BIN"), "CONXIAN_KUBO_BIN not configured")
class IndependentIPFSRestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.kubo = os.environ["CONXIAN_KUBO_BIN"]
        self.release = self.root / "release"
        self.receipt = export(self.release, self.kubo)
        self.source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()

    def check(self, **overrides):
        args = {"car": self.release / "site.car", "source_sha": self.source,
                "expected_cid": self.receipt["root_cid"],
                "expected_car_sha256": self.receipt["car_sha256"], "kubo": self.kubo}
        args.update(overrides)
        return verify(**args)

    def test_restores_from_car_without_trusting_adjacent_site_or_receipt(self):
        (self.release / "release.json").write_text('{"production_acceptance":true}')
        (self.release / "site/index.html").write_text("untrusted adjacent content")
        result = self.check()
        self.assertTrue(result["offline_restoration_verified"])
        self.assertFalse(result["live_replication_verified"])
        self.assertFalse(result["operator_independence_verified"])
        self.assertFalse(result["production_acceptance"])

    def test_changed_car_rejects_even_with_successful_export_receipt(self):
        with (self.release / "site.car").open("ab") as handle:
            handle.write(b"changed")
        with self.assertRaises(ValueError):
            self.check()

    def test_wrong_source_pin_rejects(self):
        with self.assertRaises(ValueError):
            self.check(source_sha="f" * 40)

    def test_wrong_cid_is_not_retrieved_from_the_network(self):
        with self.assertRaises(subprocess.SubprocessError):
            self.check(expected_cid="bafybeiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def test_symlink_archive_is_rejected(self):
        link = self.root / "alias.car"
        link.symlink_to(self.release / "site.car")
        with self.assertRaises(OSError):
            self.check(car=link)

    def test_incomplete_pins_are_not_accepted(self):
        for kwargs in [{"source_sha": "main"}, {"expected_cid": "latest"},
                       {"expected_car_sha256": ""}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.check(**kwargs)


if __name__ == "__main__":
    unittest.main()
