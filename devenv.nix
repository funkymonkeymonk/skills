{ pkgs, ... }:

{
  packages = [ pkgs.python3 pkgs.git pkgs.gh ];

  tasks."skills:vendor" = {
    exec = "python3 scripts/vendor_skills.py sync --manifest upstreams.json --repo .";
  };

  tasks."upstreams:check" = {
    exec = ''
      python3 scripts/vendor_skills.py update \
        --manifest upstreams.json \
        --repo . \
        --base main \
        --repo-slug funkymonkeymonk/skills
    '';
  };

  tasks."check:lint" = {
    exec = ''
      export PYTHONDONTWRITEBYTECODE=1
      python3 -m unittest discover -s tests -v
      bash tests/check-docs-skill.sh
      bash tests/check-reversible-decisions.sh
      if command -v ste >/dev/null 2>&1; then
        ste lint --mode=flavored --format=agent --no-config \
          README.md \
          docs/how-to/vendor-a-superpowers-skill.md \
          docs/explanation/decisions/0003-selective-superpowers-skill-vendoring.md \
          docs/reference/specifications/2026-11-08-superpowers-skill-vendoring-design.md \
          docs/reference/specifications/2026-11-07-diataxis-ste-docs-design.md \
          docs/reference/specifications/2026-11-08-reversible-decisions-design.md
      fi
    '';
  };
}
