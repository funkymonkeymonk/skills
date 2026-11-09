import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMPORTED = {
    "consumer-decision-guides",
    "creating-user-manual",
    "devenv",
    "ste-implementation-plans",
}


class ImportedNixSkillTests(unittest.TestCase):
    def test_selected_skills_have_matching_agent_skill_metadata(self):
        for name in sorted(IMPORTED):
            with self.subTest(skill=name):
                skill_file = ROOT / "skills" / name / "SKILL.md"
                self.assertTrue(skill_file.is_file(), f"missing {skill_file}")
                text = skill_file.read_text()
                frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
                self.assertIsNotNone(frontmatter, f"missing frontmatter in {skill_file}")
                self.assertRegex(frontmatter.group(1), rf"(?m)^name:\s*{re.escape(name)}\s*$")
                self.assertRegex(frontmatter.group(1), r"(?m)^description:\s*\S")

    def test_devenv_skill_keeps_its_reference_guides(self):
        base = ROOT / "skills" / "devenv"
        for name in ("basics.md", "tasks.md", "scripts.md", "packages.md"):
            self.assertTrue((base / name).is_file(), f"missing devenv guide {name}")

    def test_ste_plan_skill_has_a_distinct_explicit_trigger(self):
        text = (ROOT / "skills" / "ste-implementation-plans" / "SKILL.md").read_text()
        self.assertIn("when a user explicitly requests", text)
        self.assertIn("writing-plans", text)
        self.assertIn("ste lint", text)

    def test_readme_and_adr_record_the_imported_skills(self):
        readme = (ROOT / "README.md").read_text()
        for name in sorted(IMPORTED):
            self.assertIn(f"`{name}`", readme)
        adr = ROOT / "docs" / "explanation" / "decisions" / "0004-nix-skill-imports.md"
        self.assertTrue(adr.is_file())
        text = adr.read_text()
        self.assertIn("Keep `funkymonkeymonk/nix` unchanged", text)
        self.assertIn("ste-implementation-plans", text)


if __name__ == "__main__":
    unittest.main()
