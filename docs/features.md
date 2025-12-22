Feature Design & Evaluation Principles

This engine uses a classical, interpretable evaluation composed of many small features. Features are designed with the following principles:

## Side-Local Evaluation

Most features evaluate one side in isolation.

Final contribution is computed as:
feature_score = white_score − black_score.

This preserves symmetry, simplifies testing, and integrates cleanly with negamax.

Truly relational features (e.g. tempo, initiative) are allowed but should be rare.

## Natural Scaling Before Weighting

Each feature must have a natural centipawn range appropriate to its concept.

Scaling errors should be fixed at the feature level, not by extreme weights.

After proper scaling, weights should be small and boring (≈ 0.5–1.5).

## Category Budgets

Features are grouped into conceptual categories (material, pawn structure, space, king safety, etc.).

Each category has an implicit maximum budget (e.g. space ≈ ±100 cp).

Adding new features to a category should refine how the budget is allocated, not increase the total.

## Caps Over Global Scaling

Prefer per-feature caps and diminishing returns over scaling everything down.

Features within a category should compete, not stack unchecked.

Scaling all features by 1/N when adding new ones is discouraged.

## Avoid Double-Counting

A feature should answer:
“How good is this position for this side?”

Do not embed opponent weaknesses inside a side’s score; subtraction handles that.

Highly correlated features should be merged, averaged, or dampened.

## Phase Awareness

Feature relevance depends on game phase.

Use phase-based multipliers (opening / middlegame / endgame) instead of changing weights.

Example: king safety fades in endgame; king activity grows.

## Debuggability & Sanity Checks

Feature outputs should be human-explainable (“~½ pawn advantage”).

Logging per-feature contributions is expected and encouraged.

Rule of thumb:

> Features define what matters, scaling defines how much, and weights only fine-tune importance.

## Feature Budgets

Target evaluation for features in each category, measured in centipawns

| Category                | Budget (cp) |
| ----------------------- | ----------- |
| Material                | ±2500       |
| Pawn structure          | ±200        |
| Space                   | ±100        |
| Activity / mobility     | ±200        |
| King safety             | ±300        |
| King activity (endgame) | ±200        |
| Initiative / tempo      | ±30         |
| Tactical penalties      | ±800 (cap)  |
| Endgame conversion      | ±300        |
