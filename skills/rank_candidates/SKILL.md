---
name: rank_candidates
description: Score and rank a list of candidate profiles against a job requirement using semantic similarity. ALWAYS call this skill IMMEDIATELY after linkedin_search returns candidates, to reorder them by best fit. Pass the candidates and the original role description. Returns the same list with a "score" (0-100) field added, sorted highest first.
---

# rank_candidates

## What this skill does
Ranks candidates by how well their headline matches the job requirement. Uses sentence embeddings (semantic similarity) so it understands related concepts — knows Django and Flask are Python frameworks even if those words aren't in the original query.

## When to use
ALWAYS call this skill IMMEDIATELY after linkedin_search returns candidates. Pass the candidate list and the original role string. Then show the ranked results to the user.

## How to call it
Programmatically:
    from rank import run
    ranked = run(candidates=[...], role="Python Django Developer")

Standalone test:
    cd {baseDir}
    python rank.py

## Input
- candidates: list of dicts with at least "name" and "role" fields
- role: string describing the job being hired for

## Output
Same list of dicts, sorted by score descending, with a new "score" field (0-100) added to each.

## Example
Input role: "Python Django Developer"
Input candidates:
- {name: "X", role: "Python, Django Developer at Flipkart"}
- {name: "Y", role: "Frontend React Engineer"}

Output (sorted highest first):
- {name: "X", role: "Python, Django Developer at Flipkart", score: 87}
- {name: "Y", role: "Frontend React Engineer", score: 32}
