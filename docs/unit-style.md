# Unit Style

This guide defines how measurements are written in recipe Ingredients, Directions, and Notes. The goal is consistent text, not unit conversion: a tablespoon should look the same in every recipe.

Applies to all files under `recipes/`. Agents editing recipes must follow this guide.

## Quick reference

| Element | Standard | Example |
|---|---|---|
| Tablespoon | `tbsp` (lowercase, no period) | `2 tbsp olive oil` |
| Teaspoon | `tsp` (lowercase, no period) | `1/2 tsp salt` |
| Ounce | `oz` (no period) | `8 oz pasta` |
| Pound | `lb` (no period) | `1 lb ground turkey` |
| Cup | `cup`, plural `cups` when more than 1 | `1 cup flour`, `1 1/2 cups water` |
| Fractions | ASCII, never glyphs | `1/2`, `1 1/2`, `3/4` (not `½`, `1½`) |
| Ranges | hyphen, no spaces | `2-3 garlic cloves`, `10-12 minutes` |
| Garlic | `N garlic cloves` | `4 garlic cloves, minced` |
| Cans, jars, packages | `N (X oz) can` / `cans` | `2 (15 oz) cans chickpeas`, `1 (14 oz) can tomatoes` |
| Temperature | number + `°F` | `Preheat oven to 350°F` |
| Number and unit | one space | `7 g yeast`, not `7g yeast` |

## Rules

### Abbreviations
- Use `tbsp`, `tsp`, `oz`, `lb`, `cup`, `g`, `ml`, `mg`. Never `Tbsp.`, `tsp.`, `T`, `c.`, `tablespoons`, `ounces`, `pounds`, `grams`, or `milliliters`.
- Because `tbsp`, `tsp`, `oz`, and `lb` never change, `2 tbsp` and `1 tbsp` look the same. `cup` is the only unit that pluralizes.

### Fractions and quantities
- Use ASCII fractions. Unicode glyphs (`½`, `¼`, `¾`, `⅓`, `⅔`, `⅛`) are not used in recipe text.
- Mixed numbers have one space: `1 1/2`.
- Use digits, not words, for quantities: `2 cloves`, not `two cloves`. This includes count words before cans and packages (`Two 15-oz cans` becomes `2 (15 oz) cans`).

### Ranges
- Use a hyphen between numbers: `2-3 tbsp`, `10-12 minutes`, `1 1/2-2 lb`.
- Do not use `to` or en dashes between numbers. Words like `to taste` and `to serve` are unaffected.

### Cans, jars, packages
- Put the size in parentheses before the container word: `2 (15 oz) cans`, `1 (28 oz) can`, `1 (12 oz) package`.
- Count-word forms are converted to digits: `Two 15-oz cans` becomes `2 (15 oz) cans`.

### Garlic
- Write `4 garlic cloves`, not `4 cloves garlic`. Size words come before `garlic`: `1 large garlic clove`.

### Temperatures
- Write `350°F`, with the degree symbol directly attached to `F`.
- Do not write `degrees`, `degrees F`, or `°` alone.

### Metric
- Where imperial is the primary measure, remove metric parenthetical conversions such as `(240 g)` or `(1 L)`.
- Baking recipes where weight is specified keep the gram weight: `1 cup (125 g) flour`.
- Metric-only lines stay metric and use the same spacing: `7 g`, `85 g`, `750 ml`. Do not add imperial conversions.
- Nutrition labels use the same spacing: `12 g fat`, `75 mg cholesterol`, `206 kcal`.

## Not yet standardized

These are open. Do not change them without a decision:
- `pinch`, `to taste`, `as needed`, and size words such as `large`, `medium`, `small`.
- Inch marks: `1" piece` vs `1-inch piece`.
- Slash weight form: `1 cup/130 g` (Chocolate-Stuffed Oatmeal Cookies).

## Applying this guide
- Make the smallest edit that brings the text into line. Do not change ingredient names, quantities, or meaning.
- Keep frontmatter and photo embeds unchanged. This guide covers the body text only, plus the `servings`, `cook_time`, `prep_time`, and `total_time` values.
- After editing, run `paprika-recipes status` and check the diff for unintended changes.
