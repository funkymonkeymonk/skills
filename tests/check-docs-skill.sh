#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

required_files=(
  AGENTS.md
  README.md
  .gitignore
  skills/diataxis-docs/SKILL.md
  docs/reference/specifications/2026-11-07-diataxis-ste-docs-design.md
  docs/explanation/decisions/0001-repo-local-documentation-policy.md
  tests/fixtures/documentation-pressure-test.md
  tests/fixtures/ste-opt-out-test.md
)

missing=()
for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    printf 'Missing required file: %s\n' "$path" >&2
    missing+=("$path")
  fi
done

if (( ${#missing[@]} > 0 )); then
  exit 1
fi

grep -Fxq '/plans/' .gitignore
grep -Fxq '/.pi-subagents/' .gitignore
grep -Fxq '/ASD-STE100_ISSUE9.pdf' .gitignore
grep -Fq 'docs/reference/specifications/' AGENTS.md
grep -Fq 'docs/explanation/decisions/' AGENTS.md
grep -Fq 'Use STE unless the user explicitly requests another style.' skills/diataxis-docs/SKILL.md
