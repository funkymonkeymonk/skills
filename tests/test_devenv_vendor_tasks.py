import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVENV = ROOT / "devenv.nix"


class DevenvVendorTaskTests(unittest.TestCase):
    def test_devenv_defines_sync_update_and_required_check_tasks(self):
        self.assertTrue(DEVENV.is_file(), "devenv.nix must define repository tasks")
        config = DEVENV.read_text()
        self.assertIn('tasks."skills:vendor"', config)
        self.assertIn('tasks."upstreams:check"', config)
        self.assertIn('tasks."check:lint"', config)
        self.assertIn("pkgs.python3", config)
        self.assertIn("pkgs.git", config)
        self.assertIn("pkgs.gh", config)
        self.assertIn("scripts/vendor_skills.py sync", config)
        self.assertIn("scripts/vendor_skills.py update", config)

    def test_readme_and_how_to_use_the_devenv_tasks(self):
        readme = (ROOT / "README.md").read_text()
        guide = (ROOT / "docs" / "how-to" / "vendor-a-superpowers-skill.md").read_text()
        self.assertIn("devenv tasks run skills:vendor", readme)
        self.assertIn("devenv tasks run skills:vendor", guide)
        self.assertIn("devenv tasks run upstreams:check", guide)


if __name__ == "__main__":
    unittest.main()
