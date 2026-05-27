# Create Repo

You are bootstrapping a new project with the SDLC pipeline.

## Arguments

The user provides a path in the form `[path]\[project-name]` or `[path]/[project-name]`. This is the target directory for the new project.

If no argument is provided, ask the user for the target path.

## Steps

### 1. Parse and validate target

- Extract the target path from the argument.
- Resolve it to an absolute path.
- If the target directory already exists, **stop with an error**: "Target directory already exists: `{path}`. Will not overwrite. Choose a different name or remove the existing directory."

### 2. Create project structure

Create the following directory structure at the target:

```
{project-name}/
├── sdlc/
│   ├── docs/
│   └── prompts/
│       ├── SKILL.md
│       ├── create-repo.md
│       ├── draft-user.md
│       ├── draft-pdr.md
│       ├── draft-plan.md
│       ├── gen-pdr.md
│       ├── gen-plan.md
│       ├── finalize.md
│       ├── expand.md
│       ├── implement.md
│       └── prompt-instructions.md
└── .gitignore
```

### 3. Copy SDLC prompts

Copy all prompt files from this installation's `skill/` directory into the new project's `sdlc/prompts/` directory. These files are:

- `SKILL.md`
- `create-repo.md`
- `draft-user.md`
- `draft-pdr.md`
- `draft-plan.md`
- `gen-pdr.md`
- `gen-plan.md`
- `finalize.md`
- `expand.md`
- `implement.md`
- `prompt-instructions.md`

Read each file from the source location and write it to the target location. The prompts must be self-contained — they should work in the new project without any reference back to this template repo.

### 4. Create .gitignore

Write a basic `.gitignore` at the project root:

```
__pycache__/
*.pyc
*.egg-info/
dist/
build/
.eggs/
.venv/
venv/
```

### 5. Initialize git (optional)

Run `git init` in the new project directory to set up version control.

### 6. Report success

Output:
```
Created project: {project-name}
Location: {absolute-path}

Next steps:
1. cd {absolute-path}
2. Describe your project requirements
3. Run /sdlc draft-user to capture them as a requirements doc
4. Run /sdlc gen-pdr to generate a physical design
5. Run /sdlc gen-plan to create an implementation plan
6. Run /sdlc finalize to finalize all documents
7. Run /sdlc expand to generate phase plans
8. Run /sdlc implement to execute the plan
```

## Error Handling

- Target exists -> error, stop immediately
- Cannot create directory (permissions) -> error with the OS message
- Cannot copy a prompt file -> warn but continue with the rest
