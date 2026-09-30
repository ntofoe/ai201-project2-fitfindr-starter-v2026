# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 rather than 5 of 5 because query parsing is regex-based. Some
natural phrasings won't match my "under $N" or "size X" patterns cleanly — a
query that omits the dollar sign, or phrases size differently, could cause an
occasional parse miss even when a matching listing genuinely exists.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
5 of 5 is reasonable here because this path depends only on search_listings
returning an empty list and the branch correctly stopping — a deterministic
check with no fuzzy matching involved. If the branch logic is correct, it
should behave identically on every run, unlike criterion 1's dependency on
parsing real-world phrasing.

---

## 3. The selected item reaches suggest_outfit unchanged

For at least 5 of 5 runs, the `id` field of `session["selected_item"]` matches
the `id` field of the item passed into `suggest_outfit`.

**Why this target:**

This is a state-integrity check, not a content check — either the same item
reference survives the handoff between tool calls, or it doesn't. There's no
reasonable case where it should sometimes fail, so 5 of 5 is the right bar.


---

## 4. The fit card mentions the item's price

For at least 4 of 5 different items, the generated fit card mentions the
item's price.

**Why this target:**

The fit card's wording varies since it calls the model, but the price is a
fact that should reliably appear regardless of phrasing. I chose 4 of 5 rather
than 5 of 5 because the model occasionally omits specific details even when
instructed to include them — a known limitation of prompting rather than a
bug in my code.

---

## 5. Size matching respects messy, real-world size formats

For at least 4 of 5 size-based queries, every returned listing's size field
contains the queried size as a token (after splitting on "/" and whitespace).

**Why this target:**

This tests custom logic I wrote specifically to handle inconsistent size
formatting in the data ("S/M", "W30 L30", "XL (oversized)"). Unlike a simple
price comparison, token-based string matching has real room for edge-case
bugs, so this is worth testing deliberately. I chose 4 of 5 rather than 5 of 5
because an unusual size format I haven't anticipated could cause an occasional
miss even when the underlying logic is sound.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
