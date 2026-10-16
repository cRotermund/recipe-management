# Agent Instructions

## Scope

This workspace contains a Paprika recipe working directory. The installed `paprika-recipes` command is the authority for operations; it is an external dependency (see [Tooling in `README.md`](README.md#tooling) for the upstream URL and pinned version). The workspace-specific overview is in [`README.md`](README.md), and the tool's complete behavior is documented in the upstream repository.

Recipe measurement and unit text must follow [`docs/unit-style.md`](docs/unit-style.md) (abbreviations, fractions, ranges, cans, garlic, temperatures, and metric rules). Apply it to any recipe you edit.

## Non-Negotiable Remote Safety Rule

**Do not send recipe data to Paprika without explicit approval from the owner after the proposed changes have been shown and reviewed.**

**Never push to a remote (including `paprika-recipes push` and `git push` to any remote) without first asking the owner for confirmation and receiving an explicit yes for that specific push.** Ask again for every push; a previous approval does not carry over to later pushes.

Never run a real `paprika-recipes push` on your own initiative. This includes edits, new recipes, photo uploads or replacements, and deletions. Approval must be obtained for the concrete push plan, not merely for making local edits.

Safe commands include `status`, `pull --dry-run`, and `push --dry-run`. A dry run must remain dry; do not follow it with a real push until approval is explicit.

## Working Directory

- Recipe root: `D:\Development\recipe-management\recipes`
- Tool source: `D:\Development\recipe-management\paprika-recipes`
- Installed executable: `paprika-recipes`
- Sync metadata: `recipes/.paprika/`
- Photo files: `recipes/attachments/`

Run recipe commands from `recipes/` where possible. If running elsewhere, use `--directory D:\Development\recipe-management\recipes`.

Do not manually edit, delete, regenerate, or “clean up” `.paprika/`. Its base recipe copies and photo state are required for reliable local change detection, merges, pull, push, and restore.

## Standard Agent Workflow

1. Inspect the current state before touching recipe files:

   ```powershell
   Set-Location D:\Development\recipe-management\recipes
   paprika-recipes status
   ```

2. If remote freshness matters, preview it without changing files:

   ```powershell
   paprika-recipes pull --dry-run
   ```

3. Make the smallest local edits that satisfy the request. Preserve recipe meaning, existing metadata, custom frontmatter, custom sections, and photo embeds unless the task explicitly changes them.

4. Re-run `paprika-recipes status` and inspect the actual file diff. Distinguish meaningful recipe changes from formatting-only changes.

5. Before any proposed upload, run:

   ```powershell
   paprika-recipes push --dry-run
   ```

   Report the exact operations and affected recipes to the owner and wait for explicit approval.

6. Immediately before a real push, re-run `paprika-recipes push --dry-run`. Approval applies only to the plan that was shown, and Paprika may have changed since. If the operations differ from the approved plan, stop and ask again.

7. Only after approval and a matching re-check, run `paprika-recipes push`. Then run `paprika-recipes status` and report the result. If the command reports conflicts, refused recipes, or unexpected operations, stop and ask for direction.

## Pull, Merge, and Restore

`pull` can update files, remove recipes deleted or trashed remotely, and merge independent local and remote edits. Always use `pull --dry-run` before a normal pull when local edits exist or when the remote state is uncertain.

If a pull creates conflict markers, resolve them in the recipe file before any push. A push with unresolved markers is refused. For overlapping non-prose fields such as title, rating, or times, the tool may leave the field unresolved rather than guessing.

To discard local changes and return tracked recipes to their last pulled state, use a targeted restore:

```powershell
paprika-recipes restore "Recipe Title"
paprika-recipes restore .\Recipe-File.md
paprika-recipes restore --all
```

Restore is local and does not contact Paprika. It cannot restore a never-pushed recipe because no base copy exists.

## Recipe Format

Use the format emitted by the tool. A recipe has YAML frontmatter, a `# Title`, optional description text, and supported sections:

- `## Ingredients`
- `## Directions`
- `## Notes`
- `## Nutritional Information`

Ingredients and other prose fields are opaque text to Paprika. Do not invent a new structured ingredient schema or assume amounts can be parsed independently. The `uid` identifies an existing recipe; filenames and directories do not.

Additional frontmatter and non-Paprika `##` sections are preserved locally but are not uploaded. Mention this limitation when proposing metadata changes. If a recipe has an image embed, the referenced file must exist directly under `attachments/`; photo changes are remote changes and must appear in the dry-run review.

## Remote Change Categories

Treat all of these as requiring approval before a real push:

- `created`: a new recipe will be added to Paprika.
- `uploaded` or modified fields: an existing recipe will be changed.
- Photo changes: a photo will be added, replaced, or removed.
- `trashed`: a local deletion will move a recipe into Paprika's trash.

The tool's deletion behavior is recoverable through Paprika's trash, but it is still a remote mutation and is never automatic for an agent.

## Useful Diagnostics

```powershell
paprika-recipes --help
paprika-recipes status --json
paprika-recipes pull --dry-run --json
paprika-recipes push --dry-run --json
```

Use `--json` when a machine-readable report is useful. `status` is offline and only reports local divergence; `pull` is what checks the server for changes.

If the directory stops being recognized as a Paprika repository, do not recreate `.paprika` or clone over it. Stop and investigate. In particular, a mismatched frontmatter prefix or removed UID metadata can make existing recipes appear to be new and could cause destructive-looking changes. The tool has safeguards, but the correct response is still to stop and review.

## Archives

`extract-archive` and `create-archive` operate on `.paprikarecipes` files and do not have the tracked repository's change detection or conflict handling. Prefer the existing cloned `recipes/` checkout for normal work. Archive commands are appropriate only when explicitly requested and should be treated as separate import/export workflows.
