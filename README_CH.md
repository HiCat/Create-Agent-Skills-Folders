# Create-Agent-Skills-Folders

这是一个用于快速创建 vibecoding 项目技能文件夹结构的工具仓库。你可以使用仓库内已存在的技能，也可以把新的技能加入到 `.projectSkills/unskills` 中进行管理。

## 功能亮点

- 提供一套示例技能文件夹，便于快速搭建项目技能结构
- 用简单的命令或界面选择并启用技能
- 将不使用的技能移动到 `.projectSkills/unskills` 以便管理

## 快速开始

克隆仓库：

```bash
git clone https://github.com/HiCat/Create-Agent-Skills-Folders.git
cd Create-Agent-Skills-Folders
```

## 使用技能

- 在新的聊天中触发技能选择：
  - Claude Code: `/select-project-skills`
  - Codex: `$select-project-skills`
- 让模型帮助筛选并选择最适合你项目的技能集合。

## 管理技能

- 添加技能：把技能文件夹放入 `.projectSkills/skills`
- 移除技能：将技能文件夹从 `.projectSkills/skills` 移到 `.projectSkills/unskills`，或直接删除
