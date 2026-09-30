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

<!-- Three or four sentences: what a user asks for, and what they get back. -->



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

- **What it does:** Takes a single new item and the user's wardrobe, and asks the model to suggest which wardrobe items would pair with it and why.
- **Inputs:**
  - `new_item` (dict) — one listing dict, in the shape `search_listings` returns
  - `wardrobe` (list of dicts) — the user's wardrobe items
- **Returns:** a list of dicts, each with `wardrobe_item` (the wardrobe item's id), `name` (the wardrobe item's name), and `reason` (a short string explaining the pairing)
- **When it has nothing:** if `wardrobe` is empty, returns general styling advice as a single-item list (e.g., `[{"wardrobe_item": None, "name": None, "reason": "<general advice>"}]`) rather than failing

### `create_fit_card`

- **What it does:** Writes a short caption someone would actually post, combining the new item and its suggested outfit pairings.
- **Inputs:**
  - `outfit` (list of dicts) — the return value of `suggest_outfit`
  - `new_item` (dict) — the same listing dict passed to `suggest_outfit`
- **Returns:** a string — the caption text
- **When it has nothing:** if `outfit` only contains general advice (no real wardrobe pairing), still writes a caption about the item alone, using the general advice as styling context

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` naming what the user could change (e.g., try a different size or raise the price ceiling) and return the session immediately — `suggest_outfit` is never called with nothing. Otherwise, take the first result from `search_results` as `session["selected_item"]`, pass it into `suggest_outfit`, then pass that result into `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex. Price is pulled from a pattern matching "under $N" (e.g., `r"under \$(\d+)"`), size from a pattern matching "size X" (e.g., `r"size\s+(\S+)"`), and the description is whatever remains of the query after stripping out the matched price and size phrases. Regex was chosen over asking the model because two of the three tools already call the model — parsing with regex keeps this step free, instant, and easy to debug, and both example queries in the starter follow a predictable "description ... size X ... under $N" shape that regex handles reliably.

**What moves through the session:** `session["query"]` (the raw user query) → `session["parsed"]` (the regex-extracted description/size/max_price) → `session["search_results"]` (everything `search_listings` returned) → `session["selected_item"]` (the first result chosen) → `session["outfit_suggestion"]` (the return value of `suggest_outfit`) → `session["fit_card"]` (the final caption string from `create_fit_card`).

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
