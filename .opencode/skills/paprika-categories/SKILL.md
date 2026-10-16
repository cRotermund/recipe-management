---
name: paprika-categories
description: Use when creating, editing, or categorizing Paprika recipes, or when the user mentions categories, tags, the category map, GUIDs/UUIDs in categories:, or the Meal/Protein/Style/Method hierarchy. Retrieves and syncs the local category GUID map from the Paprika SQLite database and governs how recipe categories: lists are written. Use ONLY for recipe categories, not general recipe writing.
---

# Paprika Categories

Paprika categories are a hierarchy, but the sync tool only carries category
UUIDs. Names and parent links exist only in the local Paprika database. This
skill keeps a local map of them and governs how recipe `categories:` lists are
written.

## Key facts (verified)

- The tool does **not** translate names to UUIDs. Whatever string is in a
  recipe's `categories:` list is sent to Paprika as-is. A name will be wrong.
  Always write **UUIDs**.
- Category names and hierarchy live in the local DB table `recipe_categories`
  (`uid`, `name`, `parent_uid`, `order_flag`).
- The DB is at `%LOCALAPPDATA%\Paprika Recipe Manager 3\Database\Paprika.sqlite`
  (WAL and SHM files may sit beside it).
- The map file is `D:\Development\recipe-management\category-guid-map.md`.
  It is generated. Do not hand-edit it.
- Recipes still carry **legacy** category UUIDs that are not in the current tree
  (about 26 distinct, used by about 318 assignments). Default policy: **drop
  them** when a recipe is recategorized, and leave untouched recipes alone.
- The one-recipe test (`Sheet Pan Supper`, Meal > Dinner) succeeded and was
  confirmed in the app. Use it as the reference pattern.

## Step 1: Sync the map

Run before any categorization work, and whenever the user says categories
changed in the app.

```powershell
python D:\Development\recipe-management\.opencode\skills\paprika-categories\sync_category_map.py --check
python D:\Development\recipe-management\.opencode\skills\paprika-categories\sync_category_map.py
```

- Paprika must be **closed**. The script refuses to run otherwise, so the
  database copy is never taken mid-write.
- `--check` reports ADDED, REMOVED, and CHANGED categories against the existing
  map without rewriting it. Use it first and show the user the result.
- The script copies the DB to `%LOCALAPPDATA%\Temp\opencode\paprika-db`. It never
  writes to the original DB.

## Step 2: Look up categories

Read `category-guid-map.md` and find the UUID by its hierarchy path, e.g.
`Meal > Dinner` -> `135D8DF8-5165-487A-9161-61345003AB1B`.

- Match on the full path, not just the leaf name. Leaf names repeat (e.g.
  `Staple/Base` appears only once, but check before assuming).
- If a category the user wants is not in the map, stop and say so. Do not
  invent a UUID.

## Step 3: Edit a recipe's categories

Target shape for `categories:` in frontmatter:

```yaml
categories:
- <Meal UUID>
- <Protein UUID>
- <Style UUID>
- <Method UUID>
```

Rules:
- One value per group (Meal, Protein, Style, Method) unless the user says
  otherwise.
- Not every recipe needs every group. A group may be omitted when it does not
  apply.
- **Style is for meal items only.** Staples (`Meal > Staple/Base`: spice blends,
  sauces, stocks, condiments, cooked grains and beans used as components,
  placeholders) get **no Style**.
- For staples, keep Protein or Method only where it identifies the ingredient
  (e.g. a chicken stock is `Protein > Chicken`; pressure-cooked beans are
  `Method > Pressure Cooker`). Otherwise omit them.
- Drop legacy UUIDs (anything not in the map) when recategorizing. Keep the
  recipe's name, body, and other frontmatter unchanged.
- Only touch the `categories:` block in the recipe file.

## Step 4: Review before any upload

This is non-negotiable and follows the workspace rules in `AGENTS.md`:

```powershell
Set-Location D:\Development\recipe-management\recipes
paprika-recipes status
paprika-recipes push --dry-run
```

- Show the user the exact recipes and categories that will change.
- Do **not** run `paprika-recipes push` without explicit approval of that
  specific plan.
- After an approved push, run `paprika-recipes status` and
  `paprika-recipes pull --dry-run` to confirm local and remote agree.

## Diagnostics

- Which categories a recipe has: read its `categories:` list and map each UUID
  back through `category-guid-map.md`.
- Recipes still on legacy categories: search `recipes/*.md` for UUIDs that are
  absent from the map.
- Map out of date: run the sync script with `--check` and show the diff.

## Known limits

- The tool never sees category names, so it cannot validate that a UUID is
  real. Validate against the map yourself.
- The map only reflects the local DB snapshot. If the user changed categories
  in the app but has not pulled or synced, the map can be stale. Run the sync
  script after Paprika is closed.
- This skill does not change category definitions (create, rename, delete).
  That still happens in the Paprika app.
