from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]


class RenderControlPlaneContainerTests(unittest.TestCase):
    def test_dockerfile_matches_declared_toolchain_and_standalone_runtime(self):
        dockerfile = (REPO_ROOT / "Dockerfile").read_text()

        self.assertEqual(dockerfile.count("FROM node:24-bookworm-slim"), 2)
        self.assertIn("pnpm@10.28.0", dockerfile)
        self.assertIn(
            "pnpm --filter @conxian/control-plane... install --frozen-lockfile --ignore-scripts",
            dockerfile,
        )
        self.assertIn("pnpm --filter @conxian/control-plane test", dockerfile)
        self.assertIn("pnpm --filter @conxian/control-plane build", dockerfile)
        self.assertIn("USER node", dockerfile)
        self.assertIn('CMD ["node", "apps/control-plane/server.js"]', dockerfile)

    def test_render_build_context_includes_only_required_workspace_surfaces(self):
        rules = {
            line.strip()
            for line in (REPO_ROOT / ".dockerignore").read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }

        required = {
            "**",
            "!Dockerfile",
            "!package.json",
            "!pnpm-lock.yaml",
            "!pnpm-workspace.yaml",
            "!apps/",
            "!apps/control-plane/",
            "!apps/control-plane/**",
            "!packages/",
            "!packages/client-sdk/",
            "!packages/client-sdk/**",
            "!packages/schemas/",
            "!packages/schemas/**",
            "**/node_modules",
            "**/.next",
            "**/.git",
        }
        self.assertTrue(required.issubset(rules), required - rules)
        self.assertNotIn("!**", rules)
        self.assertFalse(any(".env" in rule.lower() for rule in rules if rule.startswith("!")))


if __name__ == "__main__":
    unittest.main()
