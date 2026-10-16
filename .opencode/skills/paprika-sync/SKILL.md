---
name: paprika-sync
description: Use when syncing Paprika recipes with the git repo, pulling remote changes, editing recipes for push, or committing recipe history. Governs the pull-commit, edit, dry-run, approve, push, verify cycle and the merge-or-ask policy. Assumes Paprika can be edited on any device at any time, so drift is always possible.
---

# Paprika Sync

Paprika is the home of record. The git repository is a reviewable mirror and backup, kept in sync by hand. Treat drift as normal: the Paprika app can be edited from any device at any time.

## Principles

- `main` contains only content confirmed in Paprika, either pulled from it or pushed to it. Never commit unpushed recipe edits to `main`.
- `git log` alone does not describe current remote state. Only `pull` checks the server.
- Every write to Paprika requires owner approval of a specific dry-run plan (see `AGENTS.md`).

## Locations

- Recipe commands: run from `D:\Development\recipe-management\recipes`.
- Git commands: run from `D:\Development\recipe-management` (the `.git` directory is at the workspace root, not in `recipes/`). Use `git -C D:\Development\recipe-management ...` to avoid changing directories.

## Commit Labels

- `paprika: pull <YYYY-MM-DD HH:MM>`: inbound changes from Paprika, committed after `pull`.
- `push: <summary>`: committed only after a confirmed successful `push`, naming affected recipes and operations.

Unpushed local edits stay as working-tree changes. They are not committed to `main`.

## Step 1: Session Start (always)

```powershell
Set-Location D:\Development\recipe-management\recipes
paprika-recipes pull --dry-run
```

- If the dry run shows remote changes and no local edits exist, run `paprika-recipes pull`, then commit from the repository root as `paprika: pull <timestamp>`.
- If local edits exist, apply Step 2 before running a real `pull`.
- Report what changed in Paprika, by recipe title.

## Step 2: Merge Policy

Attempt merges yourself. Stop and ask the owner only if the merge is destructive, meaning any of:

- A recipe is removed or trashed by the pull.
- A conflict in Ingredients or Directions where one side's text would be dropped entirely.
- A photo is removed or replaced.
- A non-prose field (title, rating, times) is left unresolved by the tool.
- More than 10 lines in a single recipe change as a result of the merge.

For anything else (formatting, additive changes from both sides, clean auto-merges), resolve it and report what was merged.

Conflict markers must be resolved in the recipe file before any push. A push with unresolved markers is refused.

## Step 3: Edit

- Make the smallest edits that satisfy the request.
- Preserve frontmatter, custom sections, and photo embeds unless the task changes them.
- Re-run `paprika-recipes status` and inspect the actual diff. Separate meaningful changes from formatting-only changes.

## Step 4: Dry Run and Approval

```powershell
paprika-recipes status
paprika-recipes push --dry-run
```

Report the exact operations (created, uploaded, photo changes, trashed) and affected recipes. Wait for explicit approval of that plan.

## Step 5: Re-check Before Push

Approval applies to the plan that was shown, and the remote may have changed since the dry run. Immediately before a real push:

```powershell
paprika-recipes push --dry-run
```

If the operations differ from the approved plan, stop and ask again. Do not push.

## Step 6: Push

Only after approval and a matching re-check:

```powershell
paprika-recipes push
```

If the push reports conflicts, refusals, or unexpected operations, stop and ask for direction.

## Step 7: Verify and Commit

```powershell
paprika-recipes status
paprika-recipes pull --dry-run
```

- `pull --dry-run` should report no outstanding remote changes. This is the only check that confirms Paprika and git agree.
- Commit the pushed recipes as `push: <summary>` from the repository root.

## Restore

To discard local edits and return to the last synchronized state (no Paprika contact):

```powershell
paprika-recipes restore "Recipe Title"
paprika-recipes restore --all
```

A never-pushed recipe cannot be restored.

## Do Not

- Commit unpushed recipe edits to `main`.
- Edit, delete, or regenerate `recipes/.paprika/`.
- Push, or assume prior approval covers a new push.
- Infer remote state from git history.
