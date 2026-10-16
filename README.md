# Recipe Management

This workspace is a local, editable copy of our Paprika recipe collection. It lets us search, review, organize, and improve recipes as ordinary Markdown files while keeping Paprika as the system of record.

The `paprika-recipes` tool provides two-way synchronization with Paprika. Its complete documentation is maintained upstream (see [Tooling](#tooling)); this README focuses on how this particular workspace is organized and how I use it.

## Layout

- `recipes/`: the Paprika recipe working directory.
- `recipes/*.md`: one Markdown file per recipe.
- `recipes/attachments/`: downloaded recipe photos and locally prepared replacement photos.
- `recipes/.paprika/`: tool-managed sync state. It contains the account configuration, pristine base copies, and photo bookkeeping required for change detection and three-way merges. Do not edit it manually. It is **not committed to this repository** (it contains the account email and Paprika photo URLs with signed credentials); see [Setting Up a New Clone](#setting-up-a-new-clone).
- `AGENTS.md`: instructions for AI agents working in this workspace.
- `docs/unit-style.md`: the standard syntax for measurements, fractions, ranges, and temperatures in recipe text. Follow it when editing recipes.

The synchronization tool is not vendored in this repository. See [Tooling](#tooling).

## Everyday Workflow

Run commands from the `recipes/` directory. The tool is installed globally through `pipx` and is invoked as `paprika-recipes`; the local shell alias `pap` may also be available.

### Check Local Changes

```powershell
Set-Location D:\Development\recipe-management\recipes
paprika-recipes status
```

`status` shows local recipe edits, new files, deletions, photo changes, and formatting-only changes. It does not check whether Paprika has changed since the last pull.

### Get Changes From Paprika

```powershell
paprika-recipes pull --dry-run
paprika-recipes pull
```

Use `pull --dry-run` to preview remote changes first. A normal `pull` updates local files and can merge independent local and remote edits. If it reports conflicts, resolve them before continuing.

### Edit Recipes

Recipe files use YAML frontmatter and Markdown. Paprika-owned sections are `## Ingredients`, `## Directions`, `## Notes`, and `## Nutritional Information`; prose directly under the title is the description. Other frontmatter fields and custom `##` sections are preserved locally but are not uploaded. Recipes are identified by the `uid` frontmatter field, so renaming or moving a recipe file is safe.

New recipes can be created by adding a Markdown file with a `# Title`; the tool assigns an ID when the recipe is uploaded.

### Review Before Uploading

```powershell
paprika-recipes status
paprika-recipes push --dry-run
```

Review the file changes and dry-run output. Confirm the exact recipes and operations, including new recipes, edits, photo changes, and deletions. Only proceed with a real push after approving the reviewed plan.

### Upload After Approval

After approving the reviewed plan:

```powershell
paprika-recipes push
paprika-recipes status
```

Run `status` afterward to confirm the result. If the push reports conflicts or refuses a recipe, stop and review the problem before trying again.

## Working With the Agent

The agent (OpenCode) can read, edit, and sync these recipes for you. The `paprika-sync` skill (`.opencode/skills/paprika-sync/`) defines how it does this. Here is what to expect.

### What the agent does on its own

- **Checks Paprika at the start of every session.** It runs a pull preview and, if Paprika has changed (for example, from an edit on another device), pulls those changes and commits them to `main` as `paprika: pull <timestamp>`. Changes made in the app are treated as routine.
- **Merges independent changes.** If you and Paprika both edited a recipe, the agent attempts the merge and reports what it combined.
- **Edits local files** and reports the diff.

### What the agent will ask you about

- **Destructive merges.** It stops and asks if a merge would remove a recipe, drop a whole Ingredients or Directions passage, remove or replace a photo, leave a title/rating/time unresolved, or change more than 10 lines of a single recipe.
- **Every upload.** Nothing is sent to Paprika without your explicit yes. The agent will show you the exact plan from a dry run (new recipes, edited recipes, photo changes, trashed recipes) and wait. Approval covers only that plan. If Paprika changes before the real push, the agent re-checks and asks again.

### What the agent will not do

- Commit recipe edits to `main` that have not been pushed to Paprika.
- Edit or delete the `recipes/.paprika/` sync state.
- Push based on an earlier approval for a different plan.

### How to ask for things

- Be specific about recipe titles and the change you want ("Add a note to Chicken Soup: freeze for up to 3 months").
- If you want to review before anything is saved, say so ("show me the dry run only").
- To discard local edits, ask the agent to restore the recipe (no Paprika contact).
- After a push, expect a `push: <summary>` commit on `main` and a clean `status`. If you edited in the app since the last pull, expect a `paprika: pull` commit first.

## Undoing Local Changes

`restore` returns recipes to their last synchronized local state without contacting Paprika:

```powershell
paprika-recipes restore "Recipe Title"
paprika-recipes restore .\Recipe Title.md
paprika-recipes restore --all
```

Restoring a deleted tracked file brings it back. A newly created recipe that has never been uploaded has no previous version to restore.

Deleting a tracked Markdown file moves the recipe to Paprika's recoverable trash when pushed. Review deletions carefully before uploading them.

## More Information

Consult the upstream tool documentation (see [Tooling](#tooling)) for the complete reference, including:

- Markdown and YAML frontmatter details.
- Photo embedding and `attachments/` behavior.
- Three-way merge and conflict handling.
- Frontmatter prefixes for note vaults.
- JSON output and exit codes.
- `.paprikarecipes` archive extraction and creation.
- Authentication, keyring, cache, and command-line options.

For command syntax installed on this machine, use:

```powershell
paprika-recipes --help
paprika-recipes <command> --help
```

## Cloning This Repository

`kappari/` is a git submodule, so clone with submodules included:

```powershell
git clone --recurse-submodules git@github.com:cRotermund/recipe-management.git
```

If you already cloned without it, run:

```powershell
git submodule update --init --recursive
```

## Setting Up a New Clone

`recipes/.paprika/` is local-only. On a fresh clone (or a new machine), it must be recreated before editing, or the tool cannot detect local changes against the last pull. Run:

```powershell
Set-Location D:\Development\recipe-management\recipes
paprika-recipes pull --dry-run
paprika-recipes pull
```

Do not make recipe edits in a fresh clone until `pull` has completed, and do not run `push` until `status` reports the expected state.

## Tooling

`paprika-recipes` is an external dependency, not part of this repository. Install it with:

```powershell
uv tool install paprika-recipes
# or: pipx install paprika-recipes
```

- Upstream: https://github.com/coddingtonbear/paprika-recipes
- Pinned version: `3.0.1` (source commit `8dda5d1e1f03d8404839bfad363c047324706511`)

To reverse-engineer or troubleshoot the tool's behavior, clone the upstream repository at that commit:

```powershell
git clone https://github.com/coddingtonbear/paprika-recipes
git -C paprika-recipes checkout 8dda5d1e1f03d8404839bfad363c047324706511
```
