---
name: select-project-skills
description: 列出 `.projectSkills/unskills` 下的候选技能并将选中的技能复制到 `.projectSkills/skills`。仅在用户明确要求“use select-project-skills”（或要求使用该技能）时启用。
---

# 选择项目技能

仅在用户明确要求时使用该技能。

## 流程

1) 运行列表工具生成可用技能的 CSV。
2) 了解当前项目的技术栈和工作内容（有不清晰的地方主动询问用户）。
3) 根据第2步的信息，从第1步的csv中选择合适的技能。
4) 用所选序号运行安装工具。
5) 输出简要报告说明选择的原因。

## 脚本

- `scripts/list_unskills.py`
  - 在 `.projectSkills/unskills` 下查找 `SKILL.md`（跳过 unskills 根目录下的 `SKILL.md`）。
  - 生成包含以下列的 CSV：`index, folder_path, name, description`。
  - `folder_path` 尽量使用相对项目根目录的路径。

示例：

```bash
python3 scripts/list_unskills.py \
  --unskills-dir .projectSkills/unskills \
  --output .projectSkills/unskills/skills.csv
```

- `scripts/install_skill.py`
  - 读取列表步骤生成的 CSV。
  - 将所选技能文件夹复制到 `.projectSkills/skills`，并保留 `.projectSkills/unskills` 下的子路径结构。
  - 若目标已存在，除非传入 `--overwrite`，否则拒绝覆盖。

示例：

```bash
python3 scripts/install_skill.py \
  --csv .projectSkills/unskills/skills.csv \
  --indices 1,3 \
  --project-root .
```

## 备注

- 使用 `--overwrite` 前先询问。
- 若 CSV 中 `name` 或 `description` 为空，也保持为空并继续。
