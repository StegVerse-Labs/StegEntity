#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def clean(value: str) -> str:
    out = []
    for char in value.lower():
        out.append(char if char.isalnum() or char in "-_" else "-")
    return "".join(out).strip("-") or "record"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--target-repo", required=True)
    parser.add_argument("--org-percent", default="30")
    parser.add_argument("--repo-percent", default="63")
    args = parser.parse_args()

    today = date.today().isoformat()
    name = f"{today}-{clean(args.task_id)}-{clean(args.state)}.txt"
    path = ROOT / "monitoring" / "progress-notes" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise SystemExit(f"record exists: {path}")

    path.write_text(
        "\n".join([
            "Progress note",
            "",
            f"Generated: {today}",
            f"Task: {args.task_id}",
            f"State: {args.state}",
            f"Target repo: {args.target_repo}",
            f"Org complete: {args.org_percent} percent",
            f"Repo complete: {args.repo_percent} percent",
            "",
        ]),
        encoding="utf-8",
    )
    print(path)


if __name__ == "__main__":
    main()
