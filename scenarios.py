"""
The runs your test needs. ← UNIT 4, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
the empty-search branch needs an impossible query. One about the fit card needs
the same item run more than once. Working that out is Milestone 3's first step,
and this file is where you write it down.

`run_eval.py` runs everything here five times and writes the run log — five
because your criteria are written out of five.

Three scenarios are filled in to show the shape. Add or change whatever your
own criteria need — these are a starting point, not a fixed set.
"""

SCENARIOS = [
    {
        # A query the data can match. Criterion 1.
        "name": "matching query completes",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 1,
    },
    {
        # A query nothing can match. Criterion 2 — the branch.
        "name": "impossible query stops early",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },
    {
        # A user with nothing saved. One of unit 4's three failure modes.
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
        {
        # State integrity check. Criterion 3 — does selected_item survive
        # the handoff into suggest_outfit unchanged?
        "name": "state integrity check",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        # Fit card mentions price — item 1 of 5 different items. Criterion 4.
        "name": "fit card mentions price (item 1)",
        "query": "vintage graphic tee under $30",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Fit card mentions price — item 2 of 5 different items. Criterion 4.
        "name": "fit card mentions price (item 2)",
        "query": "corduroy wide-leg pants",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Fit card mentions price — item 3 of 5 different items. Criterion 4.
        "name": "fit card mentions price (item 3)",
        "query": "track jacket under $50",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Fit card mentions price — item 4 of 5 different items. Criterion 4.
        "name": "fit card mentions price (item 4)",
        "query": "flannel shirt",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Fit card mentions price — item 5 of 5 different items. Criterion 4.
        "name": "fit card mentions price (item 5)",
        "query": "denim jacket under $60",
        "wardrobe": "example",
        "criterion": 4,
    },
    {
        # Size matching with messy format #1. Criterion 5.
        "name": "size matching: S/M",
        "query": "graphic tee size M",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # Size matching with messy format #2. Criterion 5.
        "name": "size matching: oversized",
        "query": "flannel shirt size XL",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # Size matching with messy format #3. Criterion 5.
        "name": "size matching: waist/length",
        "query": "jeans size W30",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # Size matching with messy format #4. Criterion 5.
        "name": "size matching: single letter",
        "query": "band tee size L",
        "wardrobe": "example",
        "criterion": 5,
    },
    {
        # Size matching with messy format #5. Criterion 5.
        "name": "size matching: large",
        "query": "hoodie size L",
        "wardrobe": "example",
        "criterion": 5,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems
