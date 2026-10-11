import tempfile
import unittest
from pathlib import Path

from scripts.verify_workflow_secret_inventory import (
    compare_inventory,
    load_inventory,
    scan_workflow_references,
)


class WorkflowSecretInventoryTests(unittest.TestCase):
    def test_scans_required_and_optional_secret_references(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "deploy.yml").write_text(
                "env:\n  TOKEN: ${{ secrets.DEPLOY_TOKEN }}\n"
                "  OPTIONAL: ${{ secrets.SUBMODULE_PAT || github.token }}\n",
                encoding="utf-8",
            )

            references = scan_workflow_references(workflows)

        self.assertTrue(references["DEPLOY_TOKEN"]["required"])
        self.assertFalse(references["SUBMODULE_PAT"]["required"])
        self.assertEqual(references["DEPLOY_TOKEN"]["files"], {".github/workflows/deploy.yml"})

    def test_catalog_matches_current_workflow_references(self):
        root = Path(__file__).resolve().parents[2]
        references = scan_workflow_references(root / ".github" / "workflows")
        inventory = load_inventory(root / "ops" / "workflow-credential-inventory.json")

        self.assertEqual(compare_inventory(references, inventory), ([], []))

    def test_detects_undocumented_and_no_longer_referenced_names(self):
        references = {"ACTIVE": {"required": True}}
        inventory = {
            "ACTIVE": {},
            "UNDOCUMENTED_IN_WORKFLOWS": {},
        }

        self.assertEqual(compare_inventory(references, inventory), ([], ["UNDOCUMENTED_IN_WORKFLOWS"]))

    def test_rejects_duplicate_or_incomplete_catalog_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            path.write_text(
                '{"schemaVersion":1,"entries":[{"name":"DUP","classification":"x",'
                '"rotationPlan":"x","approval":"x"},{"name":"DUP","classification":"x",'
                '"rotationPlan":"x","approval":"x"}]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate"):
                load_inventory(path)

            path.write_text('{"schemaVersion":1,"entries":[{"name":"INCOMPLETE"}]}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must include"):
                load_inventory(path)


if __name__ == "__main__":
    unittest.main()