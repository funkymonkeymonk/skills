import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "vendor_skills.py"


class VendorSkillSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self.destination = self.root / "destination"
        self.destination.mkdir()
        self._git("init", str(self.upstream))
        self._git("-C", str(self.upstream), "config", "user.name", "Test User")
        self._git("-C", str(self.upstream), "config", "user.email", "test@example.com")
        self._git("-C", str(self.upstream), "config", "commit.gpgsign", "false")
        (self.upstream / "skills" / "wanted").mkdir(parents=True)
        (self.upstream / "skills" / "wanted" / "SKILL.md").write_text("version one\n")
        (self.upstream / "LICENSE").write_text("Upstream license text\n")
        self.pin = self._commit("initial skill")
        (self.upstream / "skills" / "wanted" / "SKILL.md").write_text("version two\n")
        (self.upstream / "skills" / "unwanted").mkdir()
        (self.upstream / "skills" / "unwanted" / "SKILL.md").write_text("do not copy\n")
        self._commit("change upstream")

    def _git(self, *args):
        return subprocess.run(
            ["git", *args],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

    def _commit(self, message):
        self._git("-C", str(self.upstream), "add", ".")
        self._git("-C", str(self.upstream), "commit", "-m", message)
        return self._git("-C", str(self.upstream), "rev-parse", "HEAD")

    def _write_manifest(self, skills):
        manifest = self.root / "upstreams.json"
        manifest.write_text(json.dumps({"version": 1, "skills": skills}))
        return manifest

    def _sync(self, manifest):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "sync",
                "--manifest",
                str(manifest),
                "--repo",
                str(self.destination),
            ],
            text=True,
            capture_output=True,
        )

    def test_sync_uses_pinned_commit_and_only_selected_skill(self):
        manifest = self._write_manifest(
            [
                {
                    "name": "wanted",
                    "repository": str(self.upstream),
                    "path": "skills/wanted",
                    "license_path": "LICENSE",
                    "ref": self.pin,
                }
            ]
        )

        result = self._sync(manifest)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.destination / "skills" / "wanted" / "SKILL.md").read_text(),
            "version one\n",
        )
        self.assertFalse((self.destination / "skills" / "unwanted").exists())
        self.assertEqual(
            (self.destination / "licenses" / "upstream" / "wanted-LICENSE").read_text(),
            "Upstream license text\n",
        )

    def test_manifest_rejects_duplicate_names_unsafe_paths_and_short_pins(self):
        valid = {
            "name": "wanted",
            "repository": str(self.upstream),
            "path": "skills/wanted",
            "license_path": "LICENSE",
            "ref": self.pin,
        }
        cases = [
            ([valid, dict(valid)], "duplicate skill name"),
            ([{**valid, "path": "../outside"}], "unsafe upstream path"),
            ([{**valid, "license_path": "../LICENSE"}], "unsafe license path"),
            ([{**valid, "ref": self.pin[:12]}], "full 40-character commit SHA"),
        ]
        for skills, message in cases:
            with self.subTest(message=message):
                result = self._sync(self._write_manifest(skills))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertFalse((self.destination / "skills" / "wanted").exists())

    def test_rejects_symlinked_upstream_parent_without_changing_destination(self):
        external = self.root / "external"
        (external / "wanted").mkdir(parents=True)
        (external / "wanted" / "SKILL.md").write_text("outside repository\n")
        shutil.rmtree(self.upstream / "skills")
        (self.upstream / "skills").symlink_to(external, target_is_directory=True)
        symlink_pin = self._commit("replace skills directory with a symlink")
        existing = self.destination / "skills" / "wanted" / "SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("keep me\n")
        manifest = self._write_manifest(
            [
                {
                    "name": "wanted",
                    "repository": str(self.upstream),
                    "path": "skills/wanted",
                    "license_path": "LICENSE",
                    "ref": symlink_pin,
                }
            ]
        )

        result = self._sync(manifest)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symbolic link", result.stderr)
        self.assertEqual(existing.read_text(), "keep me\n")

    def test_empty_manifest_does_not_import_upstream_skills(self):
        manifest = self._write_manifest([])

        result = self._sync(manifest)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.destination / "skills").exists())

    def test_invalid_manifest_does_not_change_existing_skills(self):
        existing = self.destination / "skills" / "existing" / "SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("keep me\n")
        manifest = self._write_manifest(
            [
                {
                    "name": "../existing",
                    "repository": str(self.upstream),
                    "path": "skills/wanted",
                    "license_path": "LICENSE",
                    "ref": self.pin,
                }
            ]
        )

        result = self._sync(manifest)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid skill name", result.stderr)
        self.assertEqual(existing.read_text(), "keep me\n")


if __name__ == "__main__":
    unittest.main()
