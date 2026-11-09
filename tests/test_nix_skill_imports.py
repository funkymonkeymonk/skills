import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IMPORTED = {
    "consumer-decision-guides",
    "creating-user-manual",
    "devenv",
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

    def test_diataxis_skill_focuses_on_document_structure(self):
        text = (ROOT / "skills" / "diataxis-docs" / "SKILL.md").read_text()
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(frontmatter)
        self.assertIn("Diataxis form", frontmatter.group(1))
        self.assertNotIn("implementation plan", frontmatter.group(1))
        self.assertIn("Diataxis", text)
        self.assertIn("For plan structure and workflow, use `writing-plans`.", text)
        self.assertIn("ste-technical-writing", text)
        self.assertNotIn("## Write in STE", text)
        self.assertNotIn("ste lint", text)

    def test_ste_writing_skill_covers_technical_documents(self):
        skill = ROOT / "skills" / "ste-technical-writing" / "SKILL.md"
        self.assertTrue(skill.is_file(), f"missing {skill}")
        text = skill.read_text()
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(frontmatter)
        self.assertRegex(frontmatter.group(1), r"(?m)^name:\s*ste-technical-writing$")
        self.assertRegex(frontmatter.group(1), r"(?m)^description:\s*Use when .+")
        self.assertIn("Use `diataxis-docs`", text)
        self.assertIn("Use `writing-plans`", text)
        self.assertIn("If the user explicitly requests another style, use it for the prose.", text)
        self.assertIn("Do not impose STE word-choice or sentence-length rules on opted-out prose.", text)
        self.assertIn("ADRs", text)
        self.assertIn("specifications", text)
        self.assertIn("plans", text)
        self.assertIn("ste lint", text)
        self.assertIn("advisory", text.lower())
        self.assertFalse((ROOT / "skills" / "ste-implementation-plans").exists())

    def test_readme_and_adr_record_the_skill_boundaries(self):
        readme = (ROOT / "README.md").read_text()
        for name in sorted(IMPORTED):
            self.assertIn(f"`{name}`", readme)
        self.assertIn("`diataxis-docs`", readme)
        self.assertIn("`ste-technical-writing`", readme)
        self.assertIn("`writing-plans`", readme)
        adr = ROOT / "docs" / "explanation" / "decisions" / "0004-nix-skill-imports.md"
        self.assertTrue(adr.is_file())
        self.assertIn("Keep `funkymonkeymonk/nix` unchanged", adr.read_text())
        split_adr = ROOT / "docs" / "explanation" / "decisions" / "0005-documentation-skill-boundaries.md"
        self.assertTrue(split_adr.is_file(), f"missing {split_adr}")
        self.assertIn("ste-technical-writing", split_adr.read_text())


if __name__ == "__main__":
    unittest.main()
