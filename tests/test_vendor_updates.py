import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "vendor_skills.py"


class VendorSkillUpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.upstream = self.root / "upstream"
        self.upstream.mkdir()
        self._git("init", str(self.upstream))
        self._configure(self.upstream)
        (self.upstream / "skills" / "alpha").mkdir(parents=True)
        (self.upstream / "skills" / "alpha" / "SKILL.md").write_text("old\n")
        (self.upstream / "skills" / "beta").mkdir()
        (self.upstream / "skills" / "beta" / "SKILL.md").write_text("beta old\n")
        (self.upstream / "LICENSE").write_text("license\n")
        self.pinned_ref = self._commit(self.upstream, "initial")
        (self.upstream / "skills" / "alpha" / "SKILL.md").write_text("new\n")
        self.latest_ref = self._commit(self.upstream, "update alpha")

        self.remote = self.root / "remote.git"
        self._git("init", "--bare", "--initial-branch=main", str(self.remote))
        self.repo = self.root / "repo"
        self._git("clone", str(self.remote), str(self.repo))
        self._configure(self.repo)
        manifest = {
            "version": 1,
            "skills": [
                {
                    "name": "alpha",
                    "repository": str(self.upstream),
                    "path": "skills/alpha",
                    "license_path": "LICENSE",
                    "ref": self.pinned_ref,
                },
                {
                    "name": "beta",
                    "repository": str(self.upstream),
                    "path": "skills/beta",
                    "license_path": "LICENSE",
                    "ref": self.pinned_ref,
                },
            ],
        }
        (self.repo / "upstreams.json").write_text(json.dumps(manifest, indent=2) + "\n")
        self._commit(self.repo, "initial manifest")
        self._git("-C", str(self.repo), "push", "origin", "main")

        self.pr_state = self.root / "prs.json"
        self.pr_log = self.root / "created-prs.jsonl"
        self.pr_state.write_text("[]")
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        gh = self.fake_bin / "gh"
        gh.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "args = sys.argv[1:]\n"
            "state_path = os.environ['FAKE_PR_STATE']\n"
            "if args[:2] == ['pr', 'list']:\n"
            "    print(open(state_path).read())\n"
            "elif args[:2] == ['pr', 'create']:\n"
            "    if os.environ.get('FAKE_PR_CREATE_FAIL') == '1': sys.exit(3)\n"
            "    def value(key): return args[args.index(key) + 1]\n"
            "    pr = {'state': 'OPEN', 'headRefName': value('--head'), 'title': value('--title')}\n"
            "    state = json.load(open(state_path))\n"
            "    state.append(pr)\n"
            "    open(state_path, 'w').write(json.dumps(state))\n"
            "    with open(os.environ['FAKE_PR_LOG'], 'a') as log: log.write(json.dumps(pr) + '\\n')\n"
            "    print('https://example.invalid/pull/1')\n"
            "else:\n"
            "    print('unexpected gh command: ' + ' '.join(args), file=sys.stderr)\n"
            "    sys.exit(2)\n"
        )
        gh.chmod(0o755)
        self.environment = os.environ.copy()
        self.environment["PATH"] = f"{self.fake_bin}:{self.environment['PATH']}"
        self.environment["FAKE_PR_STATE"] = str(self.pr_state)
        self.environment["FAKE_PR_LOG"] = str(self.pr_log)

    def _git(self, *args):
        return subprocess.run(
            ["git", *args], check=True, text=True, capture_output=True
        ).stdout.strip()

    def _configure(self, repository):
        self._git("-C", str(repository), "config", "user.name", "Test User")
        self._git("-C", str(repository), "config", "user.email", "test@example.com")
        self._git("-C", str(repository), "config", "commit.gpgsign", "false")

    def _commit(self, repository, message):
        self._git("-C", str(repository), "add", ".")
        self._git("-C", str(repository), "commit", "-m", message)
        return self._git("-C", str(repository), "rev-parse", "HEAD")

    def _update(self):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "update",
                "--manifest",
                str(self.repo / "upstreams.json"),
                "--repo",
                str(self.repo),
                "--base",
                "main",
                "--repo-slug",
                "example/skills",
            ],
            text=True,
            capture_output=True,
            env=self.environment,
        )

    def test_update_opens_one_pull_request_with_a_skill_specific_pin(self):
        result = self._update()

        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(self.pr_state.read_text())
        self.assertEqual(len(state), 1)
        self.assertEqual(state[0]["headRefName"], f"vendor/alpha-{self.latest_ref[:12]}")
        self.assertEqual(
            len(self.pr_log.read_text().splitlines()),
            1,
            "the updater should create a review PR for the changed skill",
        )
        self.assertEqual(
            self._git("--git-dir", str(self.remote), "show", f"{state[0]['headRefName']}:skills/alpha/SKILL.md"),
            "new",
        )

    def test_license_change_also_creates_an_update_pull_request(self):
        manifest_path = self.repo / "upstreams.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["skills"][0]["ref"] = self.latest_ref
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self._commit(self.repo, "accept current skill pin")
        self._git("-C", str(self.repo), "push", "origin", "main")
        (self.upstream / "LICENSE").write_text("updated license\n")
        license_ref = self._commit(self.upstream, "update upstream license")

        result = self._update()

        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(self.pr_state.read_text())
        self.assertEqual(len(state), 2)
        branches = {pr["headRefName"] for pr in state}
        self.assertEqual(
            branches,
            {f"vendor/alpha-{license_ref[:12]}", f"vendor/beta-{license_ref[:12]}"},
        )
        for branch, name in ((branch, branch.split("/")[1].split("-")[0]) for branch in branches):
            self.assertEqual(
                self._git("--git-dir", str(self.remote), "show", f"{branch}:licenses/upstream/{name}-LICENSE"),
                "updated license",
            )

    def test_update_creates_independent_pull_requests_for_changed_skills(self):
        (self.upstream / "skills" / "beta" / "SKILL.md").write_text("beta new\n")
        beta_ref = self._commit(self.upstream, "update beta")

        result = self._update()

        self.assertEqual(result.returncode, 0, result.stderr)
        branches = {pr["headRefName"] for pr in json.loads(self.pr_state.read_text())}
        self.assertEqual(
            branches,
            {f"vendor/alpha-{self.latest_ref[:12]}", f"vendor/beta-{beta_ref[:12]}"},
        )
        self.assertEqual(len(self.pr_log.read_text().splitlines()), 2)

    def test_one_invalid_skill_does_not_discard_another_skill_update(self):
        manifest_path = self.repo / "upstreams.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["skills"].append(
            {
                "name": "missing",
                "repository": str(self.upstream),
                "path": "skills/missing",
                "license_path": "LICENSE",
                "ref": self.pinned_ref,
            }
        )
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

        result = self._update()

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing", result.stderr)
        self.assertEqual(len(self.pr_log.read_text().splitlines()), 1)
        self.assertEqual(
            json.loads(self.pr_state.read_text())[0]["headRefName"],
            f"vendor/alpha-{self.latest_ref[:12]}",
        )

    def test_repeated_update_does_not_create_a_duplicate_pull_request(self):
        first = self._update()
        second = self._update()

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(len(self.pr_log.read_text().splitlines()), 1)

    def test_open_pr_for_similar_skill_name_does_not_block_update(self):
        self.pr_state.write_text(
            json.dumps(
                [{"state": "OPEN", "headRefName": "vendor/alpha-extra-abcdef123456", "title": "other skill"}]
            )
        )

        result = self._update()

        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(self.pr_state.read_text())
        self.assertEqual(len(state), 2)
        self.assertEqual(state[-1]["headRefName"], f"vendor/alpha-{self.latest_ref[:12]}")

    def test_retries_pull_request_creation_when_branch_push_succeeded(self):
        self.environment["FAKE_PR_CREATE_FAIL"] = "1"
        first = self._update()

        self.assertEqual(first.returncode, 1)
        branch = f"vendor/alpha-{self.latest_ref[:12]}"
        self.assertTrue(
            self._git("--git-dir", str(self.remote), "rev-parse", f"refs/heads/{branch}")
        )
        self.assertFalse(self.pr_log.exists())

        self.environment.pop("FAKE_PR_CREATE_FAIL")
        retry = self._update()

        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(len(self.pr_log.read_text().splitlines()), 1)
        self.assertEqual(json.loads(self.pr_state.read_text())[0]["headRefName"], branch)

    def test_closed_candidate_is_not_reopened_but_later_revision_can_proceed(self):
        rejected_branch = f"vendor/alpha-{self.latest_ref[:12]}"
        self.pr_state.write_text(
            json.dumps([{"state": "CLOSED", "headRefName": rejected_branch, "title": "old"}])
        )
        rejected = self._update()
        self.assertEqual(rejected.returncode, 0, rejected.stderr)
        self.assertFalse(self.pr_log.exists())

        (self.upstream / "skills" / "alpha" / "SKILL.md").write_text("newer\n")
        newer_ref = self._commit(self.upstream, "later update")
        later = self._update()

        self.assertEqual(later.returncode, 0, later.stderr)
        state = json.loads(self.pr_state.read_text())
        self.assertEqual(state[-1]["headRefName"], f"vendor/alpha-{newer_ref[:12]}")
        self.assertEqual(len(self.pr_log.read_text().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
