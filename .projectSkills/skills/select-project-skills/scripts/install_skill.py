#!/usr/bin/env python3
import argparse
import csv
import shutil
from pathlib import Path


def resolve_path(base: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    return (base / path).resolve()


def parse_indices(raw_indices) -> list:
    indices = []
    for item in raw_indices:
        for part in item.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                indices.append(int(part))
            except ValueError as exc:
                raise SystemExit(f"Invalid index value: {part}") from exc
    if not indices:
        raise SystemExit("No indices provided.")
    return sorted(set(indices))


def load_csv(csv_path: Path) -> list:
    if not csv_path.is_file():
        raise SystemExit(f"CSV file not found: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if not row:
                continue
            try:
                row_index = int(row.get("index", ""))
            except ValueError:
                continue
            rows.append(
                {
                    "index": row_index,
                    "folder_path": (row.get("folder_path") or "").strip(),
                }
            )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install selected skills from CSV into .projectSkills/skills."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory).",
    )
    parser.add_argument(
        "--csv",
        default=".projectSkills/unskills/skills.csv",
        help="CSV path relative to project root.",
    )
    parser.add_argument(
        "--unskills-dir",
        default=".projectSkills/unskills",
        help="Unskills directory relative to project root.",
    )
    parser.add_argument(
        "--skills-dir",
        default=".projectSkills/skills",
        help="Skills directory relative to project root.",
    )
    parser.add_argument(
        "--indices",
        nargs="+",
        required=True,
        help="One or more indices to install (comma-separated allowed).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing destinations if they already exist.",
    )
    args = parser.parse_args()

    project_root = resolve_path(Path.cwd(), args.project_root)
    csv_path = resolve_path(project_root, args.csv)
    unskills_dir = resolve_path(project_root, args.unskills_dir)
    skills_dir = resolve_path(project_root, args.skills_dir)

    indices = parse_indices(args.indices)
    rows = load_csv(csv_path)
    index_map = {row["index"]: row for row in rows}

    missing = [idx for idx in indices if idx not in index_map]
    if missing:
        missing_list = ", ".join(str(idx) for idx in missing)
        raise SystemExit(f"Indices not found in CSV: {missing_list}")

    skills_dir.mkdir(parents=True, exist_ok=True)

    installed = []
    for idx in indices:
        folder_path = index_map[idx]["folder_path"]
        if not folder_path:
            raise SystemExit(f"Missing folder_path for index {idx}")

        src_path = resolve_path(project_root, folder_path)
        if not src_path.is_dir():
            raise SystemExit(f"Source folder not found: {src_path}")

        try:
            relative = src_path.resolve().relative_to(unskills_dir.resolve())
        except ValueError as exc:
            raise SystemExit(
                f"Source folder is not under unskills dir: {src_path}"
            ) from exc

        dest_path = skills_dir / relative
        if dest_path.exists():
            if not args.overwrite:
                raise SystemExit(f"Destination exists: {dest_path}")
            shutil.rmtree(dest_path)

        shutil.copytree(src_path, dest_path)
        installed.append(dest_path)

    for path in installed:
        print(f"Installed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
