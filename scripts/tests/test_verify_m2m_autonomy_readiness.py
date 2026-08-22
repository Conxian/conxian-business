import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "verify_m2m_autonomy_readiness.py"
LEDGER = ROOT / "audit" / "m2m_autonomy_gap_ledger.json"


class M2MReadinessLedgerTests(unittest.TestCase):
    def test_canonical_ledger_passes(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ledger_has_capability_scoped_statuses(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["gaps"]), 5)
        self.assertIn("Not Run", {gap["status"] for gap in data["gaps"]})
        self.assertNotIn("fully autonomous", data["autonomy_claim"].lower())


if __name__ == "__main__":
    unittest.main()
