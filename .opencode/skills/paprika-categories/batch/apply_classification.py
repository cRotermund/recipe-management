"""Apply a category classification CSV to recipe files.

Only the `categories:` block of each recipe's frontmatter is rewritten. The
rest of the file (other frontmatter, body, photo embeds, custom sections) is
left byte-for-byte unchanged.

Usage:
    python apply_classification.py classification.csv            # dry run
    python apply_classification.py classification.csv --write    # edit files

CSV columns: file,meal,protein,style,method
Labels must match the hierarchy in category-guid-map.md (leaf names).
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

RECIPES = Path(r"D:\Development\recipe-management\recipes")
MAP = Path(r"D:\Development\recipe-management\category-guid-map.md")

GROUP_PARENT = {"meal": "Meal", "protein": "Protein", "style": "Style", "method": "Method"}


def load_map() -> dict[str, str]:
    """Return {'Parent > Leaf': uid} from the generated map, unescaping '\\/'."""
    result: dict[str, str] = {}
    for line in MAP.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or "`" not in line or "Category (hierarchy)" in line:
            continue
        label, uid_cell = line.split(" | ", 1)
        label = label.lstrip("| ").replace("\\/", "/").strip()
        result[label] = uid_cell.strip(" |`")
    return result


def uids_for(row: dict[str, str], cats: dict[str, str]) -> list[str]:
    """Return one UID per non-blank group. A blank cell means the group is omitted."""
    out = []
    for group, parent in GROUP_PARENT.items():
        leaf = row[group].strip()
        if not leaf:
            continue
        key = f"{parent} > {leaf}"
        if key not in cats:
            raise ValueError(f"{row['file']}: unknown category '{key}'")
        out.append(cats[key])
    return out


# Matches either the block form (`categories:` followed by `- item` lines) or
# the empty inline form (`categories: []`) that Paprika writes for uncategorized
# recipes.
CATEGORIES_BLOCK = re.compile(
    r"^categories:(?: \[\]\n| *\n((?:- .*\n)*))", re.MULTILINE
)


def rewrite(text: str, uids: list[str]) -> str:
    block = "categories:\n" + "".join(f"- {u}\n" for u in uids)
    new, n = CATEGORIES_BLOCK.subn(block, text, count=1)
    if n != 1:
        raise ValueError("no single categories: block found in frontmatter")
    return new


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    cats = load_map()
    changed = unchanged = 0
    errors: list[str] = []

    with args.csv_path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            path = RECIPES / row["file"]
            if not path.exists():
                errors.append(f"missing file: {row['file']}")
                continue
            try:
                uids = uids_for(row, cats)
            except ValueError as e:
                errors.append(str(e))
                continue

            original = path.read_text(encoding="utf-8")
            try:
                updated = rewrite(original, uids)
            except ValueError as e:
                errors.append(f"{row['file']}: {e}")
                continue

            if updated == original:
                unchanged += 1
                continue
            changed += 1
            if args.write:
                path.write_text(updated, encoding="utf-8", newline="")

    mode = "WROTE" if args.write else "DRY RUN"
    print(f"{mode}: {changed} recipe(s) would change, {unchanged} already correct.")
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
