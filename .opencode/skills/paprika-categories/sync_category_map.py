"""Sync the Paprika category GUID map from the local Paprika database.

Read-only with respect to Paprika. Copies the database (and any WAL/SHM
files) to a scratch folder, reads the `recipe_categories` hierarchy from the
copy, and rewrites `category-guid-map.md` at the workspace root. Also reports
categories that were added, removed, or renamed since the previous map.

Usage (from anywhere):
    python sync_category_map.py [--check]

--check   Report differences only; do not rewrite the map file.

Refuses to run while Paprika is open, so the copy is never taken mid-write.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

DB_DIR = Path(
    __import__("os").environ.get("LOCALAPPDATA", "")
) / "Paprika Recipe Manager 3" / "Database"
DB_NAME = "Paprika.sqlite"

WORKSPACE = Path(r"D:\Development\recipe-management")
MAP_FILE = WORKSPACE / "category-guid-map.md"
SCRATCH_ROOT = Path(
    __import__("os").environ.get("LOCALAPPDATA", tempfile.gettempdir())
) / "Temp" / "opencode" / "paprika-db"


def paprika_running() -> bool:
    """True if the Paprika desktop app is running."""
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Paprika*"],
            capture_output=True,
            text=True,
            check=False,
        ).stdout
    except FileNotFoundError:
        return False
    return "Paprika" in out


def snapshot_database() -> Path:
    """Copy the database and its WAL/SHM siblings to a scratch folder."""
    SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
    src_db = DB_DIR / DB_NAME
    if not src_db.exists():
        raise SystemExit(f"Database not found: {src_db}")

    for suffix in ("", "-wal", "-shm"):
        src = DB_DIR / (DB_NAME + suffix)
        if src.exists():
            shutil.copy2(src, SCRATCH_ROOT / (DB_NAME + suffix))

    return SCRATCH_ROOT / DB_NAME


def read_categories(db_path: Path) -> dict[str, tuple[str, str | None, int | None]]:
    """Return {uid: (name, parent_uid, order_flag)} from recipe_categories."""
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT uid, name, parent_uid, order_flag FROM recipe_categories"
        ).fetchall()
    finally:
        con.close()
    return {uid: (name, parent, order) for uid, name, parent, order in rows}


def category_path(uid: str, cats: dict) -> str:
    """Build the hierarchy path, e.g. 'Meal > Dinner'. Escapes '/' in names."""
    parts: list[str] = []
    cur: str | None = uid
    seen: set[str] = set()
    while cur and cur in cats and cur not in seen:
        seen.add(cur)
        name, parent, _ = cats[cur]
        parts.append(name.replace("/", "\\/"))
        cur = parent
    return " > ".join(reversed(parts))


def render_map(cats: dict) -> str:
    lines = [
        "# Paprika category GUID map",
        "",
        "Generated from the local Paprika database by "
        "`.opencode/skills/paprika-categories/sync_category_map.py`. "
        "Do not edit by hand.",
        "",
        "Use the UID in a recipe's `categories:` list. Names are for reference "
        "only. A `/` inside a name is escaped as `\\/`.",
        "",
        "| Category (hierarchy) | UID |",
        "|---|---|",
    ]
    ordered = sorted(
        cats,
        key=lambda u: (
            category_path(u, cats).split(" > ")[0],
            cats[u][2] or 0,
            category_path(u, cats),
        ),
    )
    for uid in ordered:
        lines.append(f"| {category_path(uid, cats)} | `{uid}` |")
    return "\n".join(lines) + "\n"


def read_previous_map() -> dict[str, str]:
    """Parse the existing map file into {uid: path}. Empty if none exists."""
    if not MAP_FILE.exists():
        return {}
    previous: dict[str, str] = {}
    for line in MAP_FILE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or "`" not in line:
            continue
        path, uid_cell = line.split(" | ", 1)
        uid = uid_cell.strip(" |`")
        previous[uid] = path.lstrip("| ").strip()
    return previous


def report_changes(old: dict[str, str], new: dict[str, str]) -> None:
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    renamed = sorted(u for u in set(old) & set(new) if old[u] != new[u])

    if not (added or removed or renamed):
        print("No changes since the previous map.")
        return
    for uid in added:
        print(f"ADDED    {new[uid]}  {uid}")
    for uid in removed:
        print(f"REMOVED  {old[uid]}  {uid}")
    for uid in renamed:
        print(f"CHANGED  {old[uid]}  ->  {new[uid]}  {uid}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="report differences only; do not rewrite the map file",
    )
    args = parser.parse_args()

    if paprika_running():
        print("Paprika is running. Close it first so the database is quiescent.")
        return 1

    db_copy = snapshot_database()
    cats = read_categories(db_copy)
    new_map = {uid: category_path(uid, cats) for uid in cats}
    old_map = read_previous_map()

    report_changes(old_map, new_map)

    if args.check:
        return 0

    MAP_FILE.write_text(render_map(cats), encoding="utf-8")
    print(f"Wrote {MAP_FILE} ({len(cats)} categories).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
