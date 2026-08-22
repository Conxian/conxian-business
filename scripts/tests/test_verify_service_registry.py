import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class ServiceRegistryTests(unittest.TestCase):
    def test_registry_verifies(self):
        result = subprocess.run([sys.executable, "scripts/verify_service_registry.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_site_is_not_runtime_api(self):
        registry = json.loads((ROOT / "ops/service-registry.json").read_text())
        public = next(item for item in registry["services"] if item["id"] == "labs-site")
        self.assertEqual(public["role"], "public-web")
        self.assertFalse(public["safeTestMode"])

if __name__ == "__main__":
    unittest.main()
