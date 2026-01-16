# Create-Agent-Skills-Folders

This repository helps you quickly create and manage the folder structure for "skills" used in vibecoding projects. You can use the skills included here or add new ones for management under `.projectSkills/unskills`.

## Highlights

- Example skill folders to help bootstrap a project's skill structure
- Simple commands or chat triggers to select and enable skills
- Move unused skills to `.projectSkills/unskills` for easy management

## Quick Start

Clone the repo:

```bash
git clone https://github.com/HiCat/Create-Agent-Skills-Folders.git
cd Create-Agent-Skills-Folders
```


## Using Skills

- Trigger skill selection in a new chat:
  - Claude Code: `/select-project-skills`
  - Codex: `$select-project-skills`
  - other: `use select-project-skills`
- Let the model help screen and pick the most suitable skills for your project.

## Managing Skills

- Add a skill: place the skill folder into `.projectSkills/skills`
- Remove a skill: move the skill folder from `.projectSkills/skills` to `.projectSkills/unskills`, or delete it

## Contributing

Feel free to open issues or PRs describing skills or improvements you'd like to add. Please follow any contribution guidelines before submitting.

## License

Add your chosen license here (for example: MIT, Apache-2.0).