#!/usr/bin/env python3
"""Synchronize explicitly pinned Agent Skills from Git repositories."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


class VendorError(Exception):
    """An invalid manifest or unsafe synchronization operation."""


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise VendorError(f"git {' '.join(args[:3])} failed: {message}")
    return result.stdout.strip()


def load_manifest(path: Path) -> list[dict[str, str]]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise VendorError(f"cannot read manifest {path}: {error}") from error

    if not isinstance(data, dict) or data.get("version") != 1:
        raise VendorError("manifest must be a JSON object with version 1")
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise VendorError("manifest 'skills' must be a list")

    names: set[str] = set()
    validated: list[dict[str, str]] = []
    for entry in skills:
        if not isinstance(entry, dict):
            raise VendorError("each skill entry must be a JSON object")
        name = entry.get("name")
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            raise VendorError(f"invalid skill name: {name!r}")
        if name in names:
            raise VendorError(f"duplicate skill name: {name}")
        names.add(name)

        repository = entry.get("repository")
        if not isinstance(repository, str) or not repository.strip():
            raise VendorError(f"skill {name}: repository must be a non-empty string")

        source_path = entry.get("path")
        if not isinstance(source_path, str):
            raise VendorError(f"skill {name}: path must be a relative path")
        pure_path = PurePosixPath(source_path)
        if (
            pure_path.is_absolute()
            or not pure_path.parts
            or any(part in {".", "..", ".git"} for part in pure_path.parts)
            or "\\" in source_path
        ):
            raise VendorError(f"skill {name}: unsafe upstream path {source_path!r}")

        license_path = entry.get("license_path")
        if not isinstance(license_path, str):
            raise VendorError(f"skill {name}: license_path must be a relative path")
        pure_license_path = PurePosixPath(license_path)
        if (
            pure_license_path.is_absolute()
            or not pure_license_path.parts
            or any(part in {".", "..", ".git"} for part in pure_license_path.parts)
            or "\\" in license_path
        ):
            raise VendorError(f"skill {name}: unsafe license path {license_path!r}")

        ref = entry.get("ref")
        if not isinstance(ref, str) or not SHA_PATTERN.fullmatch(ref):
            raise VendorError(f"skill {name}: ref must be a full 40-character commit SHA")
        validated.append(
            {
                "name": name,
                "repository": repository,
                "path": source_path,
                "license_path": license_path,
                "ref": ref,
            }
        )
    return validated


def checked_path(root: Path, relative: str, label: str) -> Path:
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if current.is_symlink():
            raise VendorError(f"{label} contains a symbolic link: {current}")
    return current


def ensure_regular_tree(source: Path) -> None:
    if not source.is_dir():
        raise VendorError(f"upstream skill path is not a directory: {source}")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise VendorError(f"upstream skill contains a symbolic link: {path}")
        if not path.is_dir() and not path.is_file():
            raise VendorError(f"upstream skill contains an unsupported file: {path}")


def materialize(entry: dict[str, str], repository_root: Path) -> None:
    destination = repository_root / "skills" / entry["name"]
    skills_root = repository_root / "skills"
    licenses_dir = repository_root / "licenses"
    licenses_root = licenses_dir / "upstream"
    license_destination = licenses_root / f"{entry['name']}-LICENSE"
    if any(
        path.is_symlink()
        for path in (skills_root, destination, licenses_dir, licenses_root, license_destination)
    ):
        raise VendorError(f"skill or license destination must not be a symbolic link: {destination}")

    with tempfile.TemporaryDirectory(prefix="vendor-skill-") as temporary:
        checkout = Path(temporary) / "upstream"
        run_git("clone", "--quiet", "--no-checkout", entry["repository"], str(checkout))
        run_git("-C", str(checkout), "checkout", "--quiet", "--detach", entry["ref"])
        actual_ref = run_git("-C", str(checkout), "rev-parse", "HEAD")
        if actual_ref != entry["ref"]:
            raise VendorError(
                f"skill {entry['name']}: checked out {actual_ref}, expected {entry['ref']}"
            )

        source = checked_path(checkout, entry["path"], "upstream skill path")
        ensure_regular_tree(source)
        source_license = checked_path(checkout, entry["license_path"], "upstream license path")
        if not source_license.is_file():
            raise VendorError(f"upstream license file does not exist: {source_license}")

        skills_root.mkdir(parents=True, exist_ok=True)
        licenses_root.mkdir(parents=True, exist_ok=True)
        staged_skill = Path(tempfile.mkdtemp(prefix=f".{entry['name']}-", dir=skills_root))
        staged_license_handle = tempfile.NamedTemporaryFile(
            prefix=f".{entry['name']}-", dir=licenses_root, delete=False
        )
        staged_license = Path(staged_license_handle.name)
        staged_license_handle.close()
        backup_skill = skills_root / f".{entry['name']}.backup-{os.getpid()}"
        backup_license = licenses_root / f".{entry['name']}.backup-{os.getpid()}"
        moved_skill = False
        moved_license = False
        installed = False
        try:
            shutil.rmtree(staged_skill)
            shutil.copytree(source, staged_skill)
            shutil.copy2(source_license, staged_license)
            if destination.exists():
                os.replace(destination, backup_skill)
            if license_destination.exists():
                os.replace(license_destination, backup_license)
            os.replace(staged_skill, destination)
            moved_skill = True
            os.replace(staged_license, license_destination)
            moved_license = True
            installed = True
        except OSError as error:
            if moved_skill and destination.exists():
                shutil.rmtree(destination)
            if moved_license and license_destination.exists():
                license_destination.unlink()
            if backup_skill.exists():
                os.replace(backup_skill, destination)
            if backup_license.exists():
                os.replace(backup_license, license_destination)
            raise VendorError(f"skill {entry['name']}: cannot install files: {error}") from error
        finally:
            if staged_skill.exists():
                shutil.rmtree(staged_skill)
            if staged_license.exists():
                staged_license.unlink()
            if installed:
                if backup_skill.exists():
                    shutil.rmtree(backup_skill)
                if backup_license.exists():
                    backup_license.unlink()


def sync(manifest_path: Path, repository_root: Path) -> None:
    entries = load_manifest(manifest_path)
    root = repository_root.resolve()
    for entry in entries:
        print(f"Syncing {entry['name']} at {entry['ref']}")
        materialize(entry, root)


def latest_path_revision(entry: dict[str, str]) -> str:
    with tempfile.TemporaryDirectory(prefix="upstream-check-") as temporary:
        checkout = Path(temporary) / "upstream"
        run_git("clone", "--quiet", entry["repository"], str(checkout))
        latest_skill_path = checked_path(checkout, entry["path"], "upstream skill path")
        ensure_regular_tree(latest_skill_path)
        latest_license_path = checked_path(checkout, entry["license_path"], "upstream license path")
        if not latest_license_path.is_file():
            raise VendorError(f"upstream license file does not exist: {latest_license_path}")
        result = subprocess.run(
            [
                "git",
                "-C",
                str(checkout),
                "log",
                "-1",
                "--format=%H",
                "HEAD",
                "--",
                entry["path"],
                entry["license_path"],
            ],
            text=True,
            capture_output=True,
        )
        if result.returncode:
            raise VendorError(f"skill {entry['name']}: cannot inspect upstream history: {result.stderr.strip()}")
        revision = result.stdout.strip()
        if not SHA_PATTERN.fullmatch(revision):
            raise VendorError(f"skill {entry['name']}: no upstream commit exists for {entry['path']}")
        ancestor = subprocess.run(
            ["git", "-C", str(checkout), "merge-base", "--is-ancestor", entry["ref"], revision],
            check=False,
            text=True,
            capture_output=True,
        )
        if ancestor.returncode == 0:
            return revision
        reverse = subprocess.run(
            ["git", "-C", str(checkout), "merge-base", "--is-ancestor", revision, entry["ref"]],
            check=False,
            text=True,
            capture_output=True,
        )
        if reverse.returncode == 0:
            return entry["ref"]
        raise VendorError(f"skill {entry['name']}: pinned revision is not on the upstream history")


def gh_json(*args: str) -> list[dict[str, str]]:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise VendorError(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise VendorError(f"gh returned invalid JSON: {error}") from error
    if not isinstance(value, list):
        raise VendorError("gh returned an invalid pull request list")
    return value


def run_gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], check=False, text=True, capture_output=True)
    if result.returncode:
        raise VendorError(f"gh {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def create_update_pr(
    entry: dict[str, str],
    revision: str,
    manifest_path: Path,
    repository_root: Path,
    base: str,
    repository_slug: str,
) -> str:
    name = entry["name"]
    branch = f"vendor/{name}-{revision[:12]}"
    worktree_parent = tempfile.TemporaryDirectory(prefix="vendor-pr-")
    worktree = Path(worktree_parent.name) / "repo"
    try:
        remote_branch = run_git(
            "-C", str(repository_root), "ls-remote", "--heads", "origin", f"refs/heads/{branch}"
        )
        if remote_branch:
            body = (
                f"Update `{name}` from `obra/superpowers` path `{entry['path']}`.\n\n"
                f"- Previous pin: `{entry['ref']}`\n- Proposed pin: `{revision}`\n\n"
                "Review the vendored diff before merging. This pull request does not merge automatically."
            )
            return run_gh(
                "pr", "create", "--repo", repository_slug, "--head", branch, "--base", base,
                "--title", f"chore: update vendored skill {name}", "--body", body,
            )
        run_git("-C", str(repository_root), "worktree", "add", "--quiet", "--detach", str(worktree), base)
        run_git("-C", str(worktree), "switch", "--quiet", "--create", branch)
        run_git("-C", str(worktree), "config", "user.name", "github-actions[bot]")
        run_git("-C", str(worktree), "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        run_git("-C", str(worktree), "config", "commit.gpgsign", "false")

        updated = dict(entry)
        updated["ref"] = revision
        materialize(updated, worktree)
        relative_manifest = manifest_path.resolve().relative_to(repository_root.resolve())
        manifest_file = worktree / relative_manifest
        manifest_data = json.loads(manifest_file.read_text())
        for skill in manifest_data["skills"]:
            if skill["name"] == name:
                skill["ref"] = revision
                break
        manifest_file.write_text(json.dumps(manifest_data, indent=2) + "\n")

        run_git(
            "-C",
            str(worktree),
            "add",
            "--",
            f"skills/{name}",
            f"licenses/upstream/{name}-LICENSE",
            str(relative_manifest),
        )
        changed = run_git("-C", str(worktree), "status", "--porcelain")
        if not changed:
            return ""
        run_git(
            "-C",
            str(worktree),
            "-c",
            "user.name=github-actions[bot]",
            "-c",
            "user.email=41898282+github-actions[bot]@users.noreply.github.com",
            "-c",
            "commit.gpgsign=false",
            "commit",
            "-m",
            f"chore: update vendored skill {name}",
        )
        run_git("-C", str(worktree), "push", "origin", branch)
        body = (
            f"Update `{name}` from `obra/superpowers` path `{entry['path']}`.\n\n"
            f"- Previous pin: `{entry['ref']}`\n- Proposed pin: `{revision}`\n\n"
            "Review the vendored diff before merging. This pull request does not merge automatically."
        )
        return run_gh(
            "pr",
            "create",
            "--repo",
            repository_slug,
            "--head",
            branch,
            "--base",
            base,
            "--title",
            f"chore: update vendored skill {name}",
            "--body",
            body,
        )
    finally:
        subprocess.run(
            ["git", "-C", str(repository_root), "worktree", "remove", "--force", str(worktree)],
            check=False,
            text=True,
            capture_output=True,
        )
        worktree_parent.cleanup()


def update(manifest_path: Path, repository_root: Path, base: str, repository_slug: str) -> int:
    entries = load_manifest(manifest_path)
    root = repository_root.resolve()
    try:
        manifest_path.resolve().relative_to(root)
    except ValueError as error:
        raise VendorError("update manifest must be inside the repository") from error
    if not entries:
        print("No upstream skills are selected.")
        return 0

    candidates: list[tuple[dict[str, str], str]] = []
    failures = 0
    for entry in entries:
        try:
            revision = latest_path_revision(entry)
            if revision == entry["ref"]:
                print(f"Current: {entry['name']} at {revision}")
            else:
                candidates.append((entry, revision))
        except VendorError as error:
            failures += 1
            print(f"Failed: {entry['name']}: {error}", file=sys.stderr)

    if not candidates:
        return 1 if failures else 0

    try:
        pull_requests = gh_json(
            "pr", "list", "--repo", repository_slug, "--state", "all", "--limit", "1000",
            "--json", "state,headRefName,title",
        )
    except VendorError:
        raise

    for entry, revision in candidates:
        name = entry["name"]
        branch = f"vendor/{name}-{revision[:12]}"
        branch_pattern = re.compile(rf"vendor/{re.escape(name)}-[0-9a-f]{{12}}$")
        relevant = [
            pr
            for pr in pull_requests
            if branch_pattern.fullmatch(str(pr.get("headRefName", "")))
        ]
        if any(str(pr.get("state", "")).upper() == "OPEN" for pr in relevant):
            print(f"Skipped: {name} has an open update pull request.")
            continue
        if any(
            pr.get("headRefName") == branch and str(pr.get("state", "")).upper() == "CLOSED"
            for pr in relevant
        ):
            print(f"Skipped rejected revision: {name} at {revision}")
            continue
        try:
            url = create_update_pr(entry, revision, manifest_path, root, base, repository_slug)
            if url:
                print(f"Created update pull request for {name}: {url}")
        except (VendorError, ValueError, OSError) as error:
            failures += 1
            print(f"Failed: {name}: {error}", file=sys.stderr)
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sync_parser = subparsers.add_parser("sync", help="sync exact manifest pins")
    sync_parser.add_argument("--manifest", type=Path, default=Path("upstreams.json"))
    sync_parser.add_argument("--repo", type=Path, default=Path.cwd())
    update_parser = subparsers.add_parser("update", help="check upstream pins and open review pull requests")
    update_parser.add_argument("--manifest", type=Path, default=Path("upstreams.json"))
    update_parser.add_argument("--repo", type=Path, default=Path.cwd())
    update_parser.add_argument("--base", default="main")
    update_parser.add_argument("--repo-slug", default=os.environ.get("GITHUB_REPOSITORY"))
    args = parser.parse_args()

    try:
        if args.command == "sync":
            sync(args.manifest, args.repo)
            return 0
        if not args.repo_slug:
            raise VendorError("set --repo-slug or GITHUB_REPOSITORY before creating pull requests")
        return update(args.manifest, args.repo, args.base, args.repo_slug)
    except VendorError as error:
        print(f"vendor-skills: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
