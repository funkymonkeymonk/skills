import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VendorSkillDocumentationTests(unittest.TestCase):
    def test_readme_links_the_upstream_skill_guide(self):
        readme = (ROOT / "README.md").read_text()
        self.assertIn("upstreams.json", readme)
        self.assertIn("docs/how-to/vendor-a-superpowers-skill.md", readme)
        self.assertIn("devenv tasks run upstreams:check", readme)

    def test_how_to_explains_pins_and_review_pull_requests(self):
        guide = ROOT / "docs" / "how-to" / "vendor-a-superpowers-skill.md"
        self.assertTrue(guide.is_file())
        text = guide.read_text()
        self.assertIn("full commit SHA", text)
        self.assertIn("Close", text)
        self.assertIn("npx skills add", text)

    def test_adr_records_the_vendoring_decision(self):
        adr = ROOT / "docs" / "explanation" / "decisions" / "0003-selective-superpowers-skill-vendoring.md"
        self.assertTrue(adr.is_file())
        text = adr.read_text()
        self.assertIn("exact Git commit", text)
        self.assertIn("private", text)
        self.assertIn("pull request", text)


if __name__ == "__main__":
    unittest.main()
