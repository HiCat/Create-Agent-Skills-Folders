#!/usr/bin/env python3
import argparse
import csv
import os
from pathlib import Path


def resolve_path(base: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    return (base / path).resolve()


def fold_block_lines(block_lines: list, style: str) -> str:
    if style == "|":
        return "\n".join(block_lines).strip()

    paragraphs = []
    current = []
    for line in block_lines:
        if line == "":
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append("")
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs).strip()


def parse_frontmatter(skill_path: Path) -> dict:
    try:
        text = skill_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return {}

    data = {}
    i = 1
    while i < end_index:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            style = value[0]
            i += 1
            block_lines = []
            block_indent = None
            while i < end_index:
                next_line = lines[i]
                if next_line.strip() == "":
                    block_lines.append("")
                    i += 1
                    continue
                indent = len(next_line) - len(next_line.lstrip(" "))
                if indent == 0:
                    break
                if block_indent is None:
                    block_indent = indent
                if indent >= block_indent:
                    block_lines.append(next_line[block_indent:])
                else:
                    block_lines.append(next_line.lstrip(" "))
                i += 1
            data[key] = fold_block_lines(block_lines, style)
            continue
        if (
            len(value) >= 2
            and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"))
        ):
            value = value[1:-1]
        data[key] = value
        i += 1
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List SKILL.md files under .projectSkills/unskills and generate a CSV."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory).",
    )
    parser.add_argument(
        "--unskills-dir",
        default=".projectSkills/unskills",
        help="Unskills directory relative to project root.",
    )
    parser.add_argument(
        "--output",
        default=".projectSkills/unskills/skills.csv",
        help="CSV output path relative to project root.",
    )
    args = parser.parse_args()

    project_root = resolve_path(Path.cwd(), args.project_root)
    unskills_dir = resolve_path(project_root, args.unskills_dir)
    output_path = resolve_path(project_root, args.output)

    if not unskills_dir.is_dir():
        raise SystemExit(f"Unskills directory not found: {unskills_dir}")

    records = []
    for dirpath, dirnames, filenames in os.walk(unskills_dir):
        if "SKILL.md" not in filenames:
            continue
        skill_dir = Path(dirpath)
        if skill_dir.resolve() == unskills_dir.resolve():
            continue
        skill_path = skill_dir / "SKILL.md"
        meta = parse_frontmatter(skill_path)
        try:
            folder_path = str(skill_dir.resolve().relative_to(project_root))
        except ValueError:
            folder_path = str(skill_dir.resolve())
        records.append(
            {
                "folder_path": folder_path,
                "name": meta.get("name", ""),
                "description": meta.get("description", ""),
            }
        )

    records.sort(key=lambda item: item["folder_path"])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["index", "folder_path", "name", "description"])
        for idx, record in enumerate(records, start=1):
            writer.writerow(
                [
                    idx,
                    record["folder_path"],
                    record["name"],
                    record["description"],
                ]
            )

    print(f"Wrote {len(records)} entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
