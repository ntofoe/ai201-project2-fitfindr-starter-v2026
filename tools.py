"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    [docstring stays as-is above]
    """
    listings = load_listings()

    # Filter by price first — cheap, exact check.
    if max_price is not None:
        listings = [item for item in listings if item["price"] <= max_price]

    # Filter by size using token matching, not substring matching.
    # "S/M" should match a search for "M"; "us 9" should NOT match "s".
    if size is not None:
        target = size.strip().upper()
        filtered = []
        for item in listings:
            tokens = item["size"].upper().replace("/", " ").split()
            if target in tokens:
                filtered.append(item)
        listings = filtered

    # Score by keyword overlap between the description and the listing's
    # title + description + style_tags.
    description_words = set(description.lower().split())
    scored = []
    for item in listings:
        searchable_text = " ".join([
            item["title"],
            item["description"],
            " ".join(item["style_tags"]),
        ]).lower()
        searchable_words = set(searchable_text.split())
        score = len(description_words & searchable_words)
        if score > 0:
            scored.append((score, item))

    # Sort by score, highest first, and return at most SEARCH_RESULT_LIMIT.
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    [docstring stays as-is above]
    """
    items = wardrobe.get("items", [])

    if not items:
        prompt = (
            f"Someone found this thrifted item: \"{new_item['title']}\" "
            f"({', '.join(new_item['colors'])}, {new_item['category']}). "
            f"They don't have a wardrobe on file yet. Suggest one or two "
            f"general outfit ideas for this item — what colors, styles, or "
            f"pieces would pair well with it."
        )
        return generate(prompt)

    wardrobe_lines = "\n".join(
        f"- {item['name']} ({item['category']}, {', '.join(item['colors'])})"
        for item in items
    )
    prompt = (
        f"Someone found this thrifted item: \"{new_item['title']}\" "
        f"({', '.join(new_item['colors'])}, {new_item['category']}).\n\n"
        f"Here is their wardrobe:\n{wardrobe_lines}\n\n"
        f"Suggest one or two specific outfit combinations using pieces they "
        f"already own, naming the pieces by name."
    )
    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    [docstring stays as-is above]
    """
    if not outfit or not outfit.strip():
        return (
            f"Found this: \"{new_item['title']}\" for ${new_item['price']} "
            f"on {new_item['platform']}. No outfit ideas yet, but it's a "
            f"solid find on its own."
        )

    prompt = (
        f"Write a short caption (two to four sentences) someone would "
        f"actually post about finding this thrifted item, in a casual, "
        f"excited tone — not a product description.\n\n"
        f"Item: \"{new_item['title']}\", ${new_item['price']}, found on "
        f"{new_item['platform']}.\n\n"
        f"Outfit ideas for it:\n{outfit}\n\n"
        f"Mention the item, its price, and the platform once each. Be "
        f"specific about the vibe rather than generic."
    )
    return generate(prompt)
