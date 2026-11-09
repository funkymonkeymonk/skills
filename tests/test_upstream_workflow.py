import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "update-upstreams.yml"
MANIFEST = ROOT / "upstreams.json"


class UpstreamWorkflowTests(unittest.TestCase):
    def test_workflow_runs_weekly_and_manually(self):
        self.assertTrue(WORKFLOW.is_file(), "the scheduled updater workflow must exist")
        workflow = WORKFLOW.read_text()
        self.assertRegex(workflow, r"(?m)^\s+schedule:")
        self.assertRegex(workflow, r"(?m)^\s+workflow_dispatch:")
        self.assertRegex(workflow, r"(?m)^\s+- cron: ['\"]?[0-9* ,/-]+['\"]?$")

    def test_workflow_uses_only_required_repository_write_permissions(self):
        self.assertTrue(WORKFLOW.is_file(), "the scheduled updater workflow must exist")
        workflow = WORKFLOW.read_text()
        self.assertRegex(workflow, r"(?m)^permissions:")
        self.assertRegex(workflow, r"(?m)^\s+contents:\s*write$")
        self.assertRegex(workflow, r"(?m)^\s+pull-requests:\s*write$")
        self.assertNotRegex(workflow, r"(?m)^\s+(issues|actions|packages):\s*write$")
        self.assertIn("scripts/vendor_skills.py update", workflow)
        self.assertIn("actions/checkout@v6", workflow)
        self.assertIn("actions/setup-python@v7", workflow)

    def test_manifest_pins_every_current_superpowers_skill(self):
        expected = {
            "brainstorming",
            "diagnosing-superpowers",
            "dispatching-parallel-agents",
            "executing-plans",
            "finishing-a-development-branch",
            "receiving-code-review",
            "requesting-code-review",
            "subagent-driven-development",
            "systematic-debugging",
            "test-driven-development",
            "using-git-worktrees",
            "using-superpowers",
            "verification-before-completion",
            "writing-plans",
            "writing-skills",
        }
        self.assertTrue(MANIFEST.is_file(), "the upstream allowlist must exist")
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(manifest["version"], 1)
        skills = manifest["skills"]
        self.assertEqual({skill["name"] for skill in skills}, expected)
        for skill in skills:
            self.assertEqual(skill["repository"], "https://github.com/obra/superpowers.git")
            self.assertEqual(skill["path"], f"skills/{skill['name']}")
            self.assertEqual(skill["license_path"], "LICENSE")
            self.assertRegex(skill["ref"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
