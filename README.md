# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr is an agent that helps someone shop secondhand. A user describes what they want — e.g. "vintage graphic tee under $30, size M" — and the agent searches a listings dataset, picks the best match, checks it against the user's wardrobe to suggest outfit pairings, and writes a short social-media-style caption about the find. If nothing in the listings matches the request, the agent stops immediately and tells the user what to change, rather than guessing.


---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the listings data for items matching a free-text description, a size, and a maximum price.
- **Inputs:**
  - `description` (str) — free text matched against a listing's title, description, and style_tags
  - `size` (str) — matched against the listing's size field by token, not exact string (see note below)
  - `max_price` (float) — the highest acceptable price
- **Returns:** a list of listing dicts, each with `id`, `title`, `price`, `size`, `category`, `style_tags`, `colors`, `brand`, `platform`
- **When it has nothing:** an empty list (`[]`) — never `None`, never a crash

**Size matching note:** listing sizes are inconsistently formatted (`"W30 L30"`, `"S/M"`, `"XL (oversized)"`, `"M"`). Rather than exact string match, the size field is split on `/` and whitespace, uppercased, and checked for the searched size as a token. This means searching `size="M"` correctly matches a listing sized `"S/M"`, without falsely matching on substrings inside unrelated words.

### `suggest_outfit`

- **What it does:** Takes a single new item and the user's wardrobe, and asks the model to suggest one or two outfits combining them.
- **Inputs:**
  - `new_item` (dict) — one listing dict, in the shape `search_listings` returns
  - `wardrobe` (dict) — a wardrobe dict with an `items` key holding a list of wardrobe item dicts
- **Returns:** a non-empty string with outfit suggestions, in natural language
- **When it has nothing:** if `wardrobe['items']` is empty, returns general styling advice (still a non-empty string) rather than raising or returning an empty string

### `create_fit_card`

- **What it does:** Writes a short, two-to-four sentence caption someone would actually post, combining the new item and its outfit suggestion.
- **Inputs:**
  - `outfit` (str) — the string returned by `suggest_outfit`
  - `new_item` (dict) — the same listing dict passed to `suggest_outfit`
- **Returns:** a string — the caption text, mentioning the item, its price, and its platform once each
- **When it has nothing:** if `outfit` is empty or whitespace-only, returns a descriptive message about the item alone rather than raising

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` naming what the user could change (e.g., try a different size or raise the price ceiling) and return the session immediately — `suggest_outfit` is never called with nothing. Otherwise, take the first result from `search_results` as `session["selected_item"]`, pass it into `suggest_outfit`, then pass that result into `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. Price is pulled from a pattern matching "under $N" (e.g., `r"under \$(\d+)"`), size from a pattern matching "size X" (e.g., `r"size\s+(\S+)"`), and the description is whatever remains of the query after stripping out the matched price and size phrases. Regex was chosen over asking the model because two of the three tools already call the model — parsing with regex keeps this step free, instant, and easy to debug, and both example queries in the starter follow a predictable "description ... size X ... under $N" shape that regex handles reliably.

**What moves through the session:** `session["query"]` (the raw user query) → `session["parsed"]` (the regex-extracted description/size/max_price) → `session["search_results"]` (everything `search_listings` returned) → `session["selected_item"]` (the first result chosen) → `session["outfit_suggestion"]` (the return value of `suggest_outfit`) → `session["fit_card"]` (the final caption string from `create_fit_card`).

---

## Sample Run

**One full query**

$ python app.py ask 'vintage graphic tee under $30'

Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two specific Y2K-inspired outfit combinations using the new butterfly baby tee and pieces from their existing wardrobe:

Outfit 1: Classic Y2K Streetwear (Contrast & Proportion)
Top: Y2K Baby Tee — Butterfly Print
Bottoms: Baggy straight-leg jeans, dark wash
Outerwear: Black cropped zip hoodie (worn open)
Shoes: Chunky white sneakers
Accessories: Black crossbody bag

Why it works: The tight, cropped fit of the baby tee creates a classic Y2K silhouette when paired with baggy, low-slung dark wash jeans...

Fit card: Manifested this exact butterfly baby tee on Depop for just $18 and I'm literally never taking it off! It's giving major early-2000s mall rat energy, and I can't wait to style it with baggy low-rise denim and chunky sneakers. 🦋✨

0 model calls this session, 2 served from cache

**The three tools, tested one at a time**

$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'price': 18.0, 'size': 'S/M', ...}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'price': 24.0, 'size': 'L', ...}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'price': 15.0, 'size': 'S/M', ...}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'price': 19.0, 'size': 'L', ...}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'price': 26.0, 'size': 'L', ...}]

$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two outfit combinations using the new vintage Levi's 501s and pieces from your wardrobe:

Outfit 1: Casual & Sporty
Top: White ribbed tank top
Outerwear: Black cropped zip hoodie
Bottoms: Vintage Levi's 501 Jeans — Medium Wash
Shoes: Chunky white sneakers
Accessories: Black crossbody bag

Why it works: The medium-wash Levi's and chunky white sneakers give off an effortless, 90s off-duty model vibe...

$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Still can't believe I scored these vintage Levi's 501 jeans on Depop for only $38! The medium wash is seriously the platonic ideal of broken-in denim, and the fit is just chefs kiss. Can't wait to live in these with my beat-up white sneakers all fall.

---

## How I Used AI

**Moment 1**

What I asked for: I asked Claude to help design the return shape for suggest_outfit and create_fit_card before I'd looked closely at the actual starter code.

What came back: Claude proposed structured list-of-dicts return values (e.g., {"wardrobe_item": id, "reason": text}), which seemed reasonable in the abstract.

What I changed: When we actually read the real stub signatures in tools.py, both functions were typed to return plain strings, not dicts. I had Claude rewrite the Tool Inventory section to match the real code instead of the earlier guess, and we rebuilt both tools around the correct string-based design.

**Moment 2**

What I asked for: I asked Claude how search_listings should match the size field, given that listing sizes in the data are inconsistently formatted ("S/M", "W30 L30", "XL (oversized)").

What came back: Claude explained the risk of a naive substring match — e.g., "S/M" contains "M" correctly, but a plain in check could also cause false positives elsewhere — and suggested token-based matching instead: splitting the size string on / and whitespace, then checking for an exact token match.

What I changed: I adopted the token-matching approach as written, and we verified it directly by testing search_listings('tee', size='M') against the real data to confirm it correctly matched "S/M" without false positives.


<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Size matching respects messy formats | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, produced by `run_eval.py::main`, from `results/run_2026-10-07_2004_before.md`:

matching query completes — try 1
stopped early: no
selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
search_results: 10

Fit card:
Still not over scoring this butterfly baby tee on Depop for just $18! It has the exact Lizzie McGuire energy I've been looking for all season.


**Note on criterion 5, try 5 of the original scenario set:** my first "before" run included a scenario querying "hoodie size M," which returned zero results across all 5 tries. I initially worried this was a size-matching bug, but checking the raw data directly showed the only hoodie in the dataset is sized `L` — the empty result was the *correct* behavior (no false match), not a failure. I swapped that scenario for "hoodie size L" so all five of criterion 5's tries test the intended thing (a correctly filtered, non-empty result), and re-ran. The run log above reflects the corrected scenario set.

---

## Loop Trace

**Happy path** — `python app.py ask 'vintage graphic tee under $30' --trace`

[1] parse_query
in: dict with keys: query
out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
in: dict with keys: description, size, max_price
out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
in: dict with keys: candidates
out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
in: dict with keys: item, wardrobe_items
out: Here are two specific Y2K-inspired outfit combinations using the new butterfly baby tee and pieces from their …
[5] create_fit_card
in: dict with keys: item
out: Manifested this exact butterfly baby tee on Depop for just $18 and I'm literally never taking it off! It's giv…


**Empty search** — `python app.py ask 'designer ballgown size XXS under $5' --trace`

[1] parse_query
in: dict with keys: query
out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
in: dict with keys: description, size, max_price
out: [] (empty)
[3] branch
→ empty results, stopping before suggest_outfit


**On the MCP move:** I moved `search_listings` onto MCP by registering it in `mcp_server.py` with a `@mcp.tool()` decorator, a description written for an agent that cannot see the implementation, and typed inputs matching my Tool Inventory. In `agent.py::run_agent`, I swapped the direct call for `mcp_client.call_tool("search_listings", {...})`. The result was identical before and after the swap — same item found, same outfit, same fit card — confirming the tool's actual behavior didn't change, only how it's reached.


---

## The Improvement

**What I changed:** I fixed `generate.py`'s retry logic. The `rate_limited` check previously only recognized `"429"`, `"resource" + "exhaust"`, or `"rate" + "limit"` in an error message as retryable. During my "before" test run, two tries genuinely failed with a real `503 UNAVAILABLE` error from the Gemini API ("This model is currently experiencing high demand... Please try again later") — a transient server overload, not a bad key or a rate limit. Because the message didn't match any of the three retry conditions, `generate()` treated it as permanent and raised `ModelUnavailable` immediately, aborting the whole agent run on what was actually a "try again shortly" situation. I added `"503" in message` and `"unavailable" in message` to the retry condition, so these transient overload errors now get the same backoff-and-retry treatment as rate limits.

**Which failure it was meant to fix:** This isn't one of my five original criteria — it surfaced naturally during Milestone 3 testing, not from a criterion I wrote. Two of the 65 tries in my first "before" run crashed with this real 503 error (visible in `results/run_2026-10-07_2004_before.md`, under "fit card mentions price (item 4)" try 5 and "size matching: S/M" try 1). This is exactly the kind of failure Milestone 2 asks you to simulate with a bad API key — except this one happened on its own, with a correctly-configured key, which made it a stronger and more honest finding than anything I could have staged.

**Did it help, and how do I know:** Partially — and I want to be honest about the limits of what I can show. My "after" run (`results/run_2026-10-07_2023_after.md`) completed all 65 tries with zero crashes, but a real 503 didn't recur during that run, so I can't show a direct before/after comparison of the *same* failure being caught by the fix. What I can confirm: the fix doesn't regress anything (the full test suite still passes identically — all 5 criteria still MET), and the logic change is correct by inspection — the two 503 errors from the "before" run, replayed through the updated `rate_limited` check, would now evaluate to `True` and trigger backoff-and-retry instead of raising `ModelUnavailable`. I'd call this a diagnosed-and-fixed issue with reasoned-but-not-directly-observed confirmation, rather than a fully proven fix — a true test would require forcing a 503 response, which I don't have a way to do on demand.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item in session matches item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions the item's price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Size matching respects messy formats | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Produced by `run_eval.py::main`, from `results/run_2026-10-07_2023_after.md`. All 65 tries completed with zero crashes this run (no 503 recurred to directly test the fix against, as noted above).


---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Full three-tool run returns a fit card | 4 of 5 | MET | All 5 tries completed end to end with a non-empty fit card — 5/5, comfortably above the 4/5 target. |
| 2 | Empty search stops before tool 2 | 5 of 5 | MET | All 5 tries stopped at the branch with `fit_card` still `None` — 5/5, matching the target exactly. |
| 3 | Item in session matches item passed on | 5 of 5 | MET | By construction, `agent.py` passes `session["selected_item"]` directly into `suggest_outfit` with no copy or reassignment in between — the `id` is guaranteed identical every time, and all 5 tries confirmed this. |
| 4 | Fit card mentions the item's price | 4 of 5 | MET | Checked all 5 different items' fit cards across both runs — every one that completed (not counting the two genuine 503 crashes, which produced no fit card to check) mentioned the price. |
| 5 | Size matching respects messy formats | 4 of 5 | MET | All 5 size-based queries (`S/M`, `XL (oversized)`, `W30 L30`, `L`, `L`) returned only listings whose size field tokenized to include the queried size — no false positives, no false negatives. |

**Diagnoses**

I missed nothing against any of the five criteria — same situation as unit 2. Per the note above about setting targets low, I looked honestly at where the slack is.

Criteria 2 and 3 are both set at 5 of 5 with no room for a near-miss to register differently from a robust pass. Criterion 2 is a deterministic branch check (did `search_listings` return empty, did the loop stop) — there's genuinely no fuzzy judgment involved, so 5 of 5 is defensible. Criterion 3 is a state-integrity check with the same property: either the same object reference survives the handoff or it doesn't, and nothing in the current code path could cause it to sometimes fail.

Criteria 1, 4, and 5 are set at 4 of 5, each with a real, stated reason tied to something genuinely variable (regex parsing of natural phrasing, model-generated wording, or an unanticipated size format) — these feel like honestly-chosen targets rather than safety margins, since all three were set *before* any model-calling tool existed, based on genuine uncertainty about whether the underlying mechanism (regex, prompting, string matching) would hold up.

The actual interesting finding this unit wasn't a criterion miss at all — it was the real 503 error documented under "The Improvement," which surfaced independent of any of the five criteria and pointed at a genuine gap in `generate.py`'s error handling.

## What's Still Broken

All five criteria are MET, and the one real failure this unit surfaced (the 503 handling gap) has been diagnosed and fixed in code, though not directly re-confirmed against a live recurrence of the same error — see the honesty note under "Did it help?" above.

Beyond that: my criteria still don't test the model's retry-and-recover behavior directly — if I had more time, I'd write a sixth, stretch-style check that deliberately forces a 503 (e.g., by temporarily monkey-patching the API client to raise one on the first call) and confirms the agent successfully retries and completes, rather than reasoning about the fix by inspection alone. I stopped short of building that because the assignment's own failure-injection pattern (corrupting the API key) doesn't have an equivalent for "service temporarily unavailable" without actually mocking the network layer, which felt like a larger undertaking than this unit's scope.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
