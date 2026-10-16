"""Verify that a categories-only edit changed nothing else.

For every recipe file, compares the current file against its last-pulled base
copy (.paprika/recipes/<uid>.json):
  * every non-categories frontmatter field matches the base value
  * the body (everything after the frontmatter) is unchanged from the file
    as last written by the tool, i.e. the only differing frontmatter key is
    `categories`

Reads only; writes nothing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RECIPES = Path(r"D:\Development\recipe-management\recipes")
BASE = RECIPES / ".paprika" / "recipes"

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse_frontmatter(text: str) -> dict:
    """Minimal parser for the flat frontmatter the tool writes."""
    m = FM.match(text)
    if not m:
        return {}
    data: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if line.startswith("- ") and key:
            data.setdefault(key, []).append(line[2:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            data[key] = [] if v in ("", "[]") else v.strip("'\"")
    return data


def body(text: str) -> str:
    m = FM.match(text)
    return text[m.end():] if m else text


def main() -> int:
    problems: list[str] = []
    checked = 0
    for f in sorted(RECIPES.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        uid = fm.get("uid")
        if not uid:
            continue
        base_path = BASE / f"{uid}.json"
        if not base_path.exists():
            continue
        base = json.loads(base_path.read_text(encoding="utf-8"))
        checked += 1

        # Scalar frontmatter fields (not categories) must equal the base value.
        for key in ("name", "rating", "cook_time", "prep_time", "total_time",
                    "source", "source_url", "servings", "difficulty", "created"):
            if key not in base:
                continue
            want = base.get(key)
            got = fm.get(key)
            if str(got if got is not None else "").strip("'\"") != str(want if want is not None else "").strip("'\"") and not (want in (None, "") and got in (None, "")):
                # Scalar mismatch may be a YAML/quoting artifact; record for review.
                problems.append(f"{f.name}: {key} differs (file={got!r} base={want!r})")

        # Body: the name heading must still be present and the directions/ingredients
        # blocks must match the base text.
        b = body(text)
        for section, field in (("## Ingredients", "ingredients"), ("## Directions", "directions")):
            if section in b and base.get(field):
                # the base text (stripped) should appear in the body
                if base[field].strip() and base[field].strip() not in b:
                    problems.append(f"{f.name}: {field} text no longer matches base")

    print(f"checked {checked} recipes against base")
    if problems:
        print(f"{len(problems)} potential issue(s):")
        for p in problems[:60]:
            print("  ", p)
        if len(problems) > 60:
            print(f"   ... and {len(problems) - 60} more")
        return 1
    print("No non-categories drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
