# Mise en Place Guide Style

Every recipe that involves prepping ingredients and then cooking opens its `## Directions` with a mise en place guide: what to cut, measure, and combine, and which dish each goes in, so the cook can work step by step without stopping to prep. Recipes with no cooking step, empty stubs, and (for now) baking are skipped. See [`mise-en-place-manifest.md`](mise-en-place-manifest.md).

The guide goes inside Directions because Paprika uploads only Ingredients, Directions, Notes, and Nutritional Information. A separate `##` section would stay local.

## Format

```
## Directions

Mise en place guide:

**Large bowl:**
- 1 onion, halved and sliced thin
- 3/4 lb mushrooms, sliced thin

**Small dish:**
- 1 tsp cumin
- 1/2 tsp salt

(original directions, unchanged)
```

- Lead-in line is exactly `Mise en place guide:` (plain text). A re-run replaces everything from that line to the blank line before the first original paragraph.
- One block per container. The container name (`Cutting board`, `Large bowl`, `Small dish`, `Measuring cup`, `Tray`, `Baking sheet`) is bold and ends in a colon, on its own line. Each item in the container is its own `- ` bullet. Keep any timing or prep note in parentheses at the end of the item it belongs to.
- A blank line separates each container block, and a blank line separates the guide from the first original paragraph.

## Rules

- **Group by moment of use.** Things that go into the pan at the same time share a container. Things added at different times get separate containers, even if they are both chopped vegetables.
- **Order by first use.** The first bullet is what the cook needs first.
- **Include:** cutting, trimming, mincing, zesting, juicing, draining and rinsing, patting dry, measuring spices and liquids, mixing marinades and dressings, setting out serving garnishes.
- **Include amounts** when a container holds part of a divided ingredient or a measured mix (`1 tsp turmeric` of 2 tsp). Skip amounts for a single whole item that is already in the Ingredients.
- **Omit** items used straight from the package or bottle (a splash of oil, salt for seasoning to taste) unless they are part of a measured mix. Omit equipment, preheating, and anything that must stay fresh until the last step.
- **Note timing that helps the cook** in a few words: `(can marinate up to 1 hour)`, `(keep cold until the end)`.
- **Add nothing that changes the recipe.** The guide restates prep the recipe already implies. Standard prep not in the original (such as soaking wooden skewers) should be rare and is called out for owner review.
- **Minimal recipes get minimal guides.** One or two bullets is fine for a simple side. Do not pad.
- **Units follow [`unit-style.md`](unit-style.md).**
- **Recipes with no Directions section or no real steps** are listed for owner review instead of being given a guide from guesswork.
- Do not change the original directions, ingredients, frontmatter, or photo embeds.
