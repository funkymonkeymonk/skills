#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

required_files=(
  AGENTS.md
  skills/reversible-decisions/SKILL.md
  tests/fixtures/reversible-choice.md
  tests/fixtures/hard-to-reverse-choice.md
  tests/fixtures/direct-hard-request.md
  tests/fixtures/unclear-reversal-choice.md
  tests/fixtures/meaningful-reversible-choice.md
  docs/reference/specifications/2026-11-08-reversible-decisions-design.md
  docs/explanation/decisions/0002-reversibility-based-decision-escalation.md
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

grep -Fq 'assess reversal cost' AGENTS.md
grep -Fq 'new skills, add a concise root AGENTS.md rule and an independent SKILL.md' AGENTS.md
grep -Fq 'name: reversible-decisions' skills/reversible-decisions/SKILL.md
grep -Fq 'description: Use when' skills/reversible-decisions/SKILL.md
grep -Fq 'jev_evaluate' skills/reversible-decisions/SKILL.md
grep -Fq 'If `jev_evaluate` is unavailable' skills/reversible-decisions/SKILL.md
grep -Fq 'A clear direct request counts as user input' skills/reversible-decisions/SKILL.md
grep -Fq 'Ruling:' skills/reversible-decisions/SKILL.md
grep -Fq 'Impact if wrong:' skills/reversible-decisions/SKILL.md
grep -Fq 'Rejected alternatives:' skills/reversible-decisions/SKILL.md
grep -Fq 'numbered options' skills/reversible-decisions/SKILL.md
lines="$(wc -l < skills/reversible-decisions/SKILL.md)"
(( lines < 500 ))
