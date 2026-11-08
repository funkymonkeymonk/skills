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

    def test_initial_manifest_has_an_empty_explicit_allowlist(self):
        self.assertTrue(MANIFEST.is_file(), "the upstream allowlist must exist")
        manifest = json.loads(MANIFEST.read_text())
        self.assertEqual(manifest, {"version": 1, "skills": []})


if __name__ == "__main__":
    unittest.main()
