"""Real offline interoperability test. Requires an explicitly selected Kubo binary."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.export_public_ipfs import export


@unittest.skipUnless(os.environ.get("CONXIAN_KUBO_BIN"), "CONXIAN_KUBO_BIN not configured")
class PublicIPFSRoundtripTests(unittest.TestCase):
    def test_reproducible_car_restores_identical_public_bytes_on_an_independent_repository(self):
        kubo = os.environ["CONXIAN_KUBO_BIN"]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first, second = root / "first", root / "second"
            receipt = export(first, kubo)
            self.assertEqual(receipt, export(second, kubo))
            self.assertEqual((first / "site.car").read_bytes(), (second / "site.car").read_bytes())
            self.assertFalse(receipt["network_publication"])
            self.assertFalse(receipt["production_acceptance"])
            env = {"PATH": os.environ.get("PATH", ""), "IPFS_PATH": str(root / "independent-operator")}

            def run(*args):
                return subprocess.check_output([kubo, "--offline", *args], env=env,
                                               stderr=subprocess.PIPE, timeout=120)

            run("init", "--profile=test")
            run("dag", "import", str(first / "site.car"))
            run("get", receipt["root_cid"], "--output", str(root / "restored"))
            restored = root / "restored"
            expected = {p.relative_to(first / "site"): p.read_bytes()
                        for p in (first / "site").rglob("*") if p.is_file()}
            actual = {p.relative_to(restored): p.read_bytes() for p in restored.rglob("*") if p.is_file()}
            self.assertEqual(expected, actual)
            self.assertEqual(json.loads(actual[Path("artifact-manifest.json")]), receipt["public_artifact"])


if __name__ == "__main__":
    unittest.main()
