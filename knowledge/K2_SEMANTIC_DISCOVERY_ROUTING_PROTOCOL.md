# K2 Semantic-UNKNOWN Discovery Routing Protocol

## Purpose

K2A intentionally left a backlog of textual sources whose `knowledge_domains` remained `["UNKNOWN"]`. Those records cannot be silently ignored, but the accepted K1 source rows must also remain auditable rather than being rewritten whenever later deep reading resolves a source.

This protocol therefore adds a **post-K1 discovery-routing overlay**.

The raw K1 record remains unchanged. K2 records only the later reviewed routing decision and derives an effective unresolved-backlog count from that overlay.

## Resolution modes

Two modes are allowed.

### SOURCE_WIDE

Use only when complete visual review establishes that the whole textual source belongs to one or more resolved semantic routes and no existing segment registry is needed to represent mixed carrier content.

Requirements:

- raw K1 `knowledge_domains == ["UNKNOWN"]`;
- `evidence_role == TEXTUAL_SOURCE`;
- canonical SHA256 matches the K1 source row;
- deep reading is `COMPLETE / VISUAL_PAGE`;
- page evidence is inside the reviewed range;
- resolved routes contain no `UNKNOWN`;
- Claim Extraction remains blocked and empirical credit remains `NONE`.

### SEGMENTED

Use when the physical PDF is a composite carrier and source-level routing would destroy provenance.

Requirements:

- every registered segment for the source is included;
- every segment is visually reviewed;
- every segment has a resolved `domain_routes` classification;
- the overlay route set must equal the union of the registered segment routes;
- `CARRIER_MATTER` may appear only in this mode;
- mixed `qimen + OUT_OF_SCOPE + CARRIER_MATTER` content is preserved rather than forced into one source-level label.

## Initial resolved sources

The first overlay resolves three previously raw-UNKNOWN Qimen carriers that had already received complete visual review:

- `QM-SRC-0022` — source-wide routing to `qimen` based on the complete review of《甲遁真授秘錄》上册;
- `QM-SRC-0023` — segmented routing because the carrier contains《甲遁真授秘錄》下册、two out-of-scope attached works, and carrier matter;
- `QM-SRC-0024` — segmented routing because the carrier contains Qimen works plus binding/blank/carrier matter.

These corrections do not retroactively turn the three sources into extra independent evidence votes and do not rewrite Wave1 selection history.

## Backlog accounting

`tools/generate_k2_unknown_textual_backlog.py` recomputes the raw textual UNKNOWN set directly from all 515 K1 source rows, validates every discovery-routing correction, and materializes:

- raw UNKNOWN textual source count;
- number resolved by reviewed K2 discovery;
- remaining unresolved count;
- resolved source IDs.

The generated state is `knowledge/K2_UNKNOWN_TEXTUAL_BACKLOG.json`.

At introduction:

- raw textual UNKNOWN = 96;
- resolved by reviewed K2 discovery = 3;
- remaining = 93.

`knowledge/K2_EVIDENCE_STATE.json` must carry exactly the same remaining count. Drift is a CI failure.

## Wave accounting rule

Discovery routing is not allowed to rewrite the historical definition of Wave1 after the fact.

A newly resolved source becomes eligible for an explicitly planned later evidence wave or other reviewed intake step according to its effective routing and lineage. It does not silently alter earlier Wave1 membership, reading-unit counts, or evidence totals.

## Epistemic boundary

Semantic routing answers **what body of knowledge the source belongs to**. It does not answer whether the source is correct.

Therefore every discovery-routing row keeps:

- `empirical_credit = NONE`;
- `claim_extraction_blocked = true`.

Routing resolution cannot be used as accuracy evidence, independent corroboration, or permission to bypass later Claim and prospective-validation gates.
