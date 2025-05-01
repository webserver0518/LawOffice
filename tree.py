#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

BRANCH = "├── "
LAST   = "└── "
PIPE   = "│   "
SPACE  = "    "

def walk(path: Path, prefix: str = "", max_depth: int = None, hide_hidden: bool = False, file=None):
    if max_depth is not None and max_depth < 0:
        return

    try:
        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        print(prefix + "⛔ [Permission Denied]", file=file)
        return

    if hide_hidden:
        entries = [e for e in entries if not e.name.startswith(".")]

    for idx, entry in enumerate(entries):
        connector = LAST if idx == len(entries) - 1 else BRANCH
        print(prefix + connector + entry.name, file=file)

        if entry.is_dir():
            new_prefix = prefix + (SPACE if connector == LAST else PIPE)
            walk(entry,
                 new_prefix,
                 None if max_depth is None else max_depth - 1,
                 hide_hidden,
                 file)

def main():
    parser = argparse.ArgumentParser(description="הדפסת עץ-תיקיות וקבצים")
    parser.add_argument("path", nargs="?", default=".", help="תיקיית בסיס (ברירת-מחדל: הנוכחית)")
    parser.add_argument("--depth", type=int, help="עומק מקסימלי (ללא הגבלה כברירת-מחדל)")
    parser.add_argument("--hide-hidden", action="store_true", help="התעלם מקבצים/תיקיות מוסתרים")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    with open("tree.txt", "w", encoding="utf-8") as f:
        print(root.name, file=f)
        walk(root,
             prefix="",
             max_depth=args.depth,
             hide_hidden=args.hide_hidden,
             file=f)

if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    main()
