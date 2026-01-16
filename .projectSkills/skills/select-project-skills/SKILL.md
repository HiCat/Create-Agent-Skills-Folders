---
name: select-project-skills
description: List candidate skills under `.projectSkills/unskills` and copy chosen skills into `.projectSkills/skills`. Use only when the user explicitly requests "use select-project-skills" (or says to use this skill).
---

# Select Project Skills

Use this skill only when the user explicitly requests it.

## Workflow

1) Run the listing tool to generate a CSV of available skills.
2) Understand the project's tech stack and current work (ask the user when anything is unclear).
3) Based on step 2, select appropriate skills from the CSV in step 1.
4) Run the install tool with the selected indices.
5) Provide a brief report explaining the selection.

## Scripts

- `scripts/list_unskills.py`
  - Find `SKILL.md` under `.projectSkills/unskills` (skips `SKILL.md` at the unskills root).
  - Write CSV with columns: `index, folder_path, name, description`.
  - `folder_path` is project-root relative when possible.

Example:

```bash
python3 scripts/list_unskills.py \
  --unskills-dir .projectSkills/unskills \
  --output .projectSkills/unskills/skills.csv
```

- `scripts/install_skill.py`
  - Read the CSV from the listing step.
  - Copy selected skill folders into `.projectSkills/skills`, preserving the subfolder path under `.projectSkills/unskills`.
  - Refuse to overwrite existing destinations unless `--overwrite` is provided.

Example:

```bash
python3 scripts/install_skill.py \
  --csv .projectSkills/unskills/skills.csv \
  --indices 1,3 \
  --project-root .
```

## Notes

- Ask before using `--overwrite`.
- If CSV entries have missing `name` or `description`, keep them blank and proceed.
