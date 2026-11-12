# THE UNDERGROWTH — MYCELIUM's Wild Hypothesis Garden

**Status:** DESIGN / PROPOSED EXPERIMENT, not deployed software or validated findings  
**Date:** 2026-11-12  
**Origin:** Conversation exploring the Obsidian relational database as an inspiration, not an authorization to alter Obsidian or Langley.

## Purpose

Create an evidence-native investigative knowledge system that can retain contradictory claims, trace their sources, propose surprising alternative explanations, and explain why any hypothesis is worth examining. It must not silently convert connections, model outputs, or agreement into verified truth.

## Foundational distinctions

- **Source:** original artifact with origin, timestamp, version/hash when available, and access/custody notes.
- **Observation:** what an examiner directly found in a particular source or environment, with scope and method.
- **Claim:** a proposition attributed to a speaker/source, not automatically endorsed.
- **Hypothesis:** a testable interpretation, explicitly unverified.
- **Relationship:** typed link with provenance and evidence references, not proof by association.
- **Finding:** synthesis preserving supporting and opposing evidence, uncertainty, dissent, and review history.
- **Decision:** human-authorized disposition, separate from an AI recommendation.

Never overwrite historical assertions silently. Maintain immutable event history and explicit supersession links. Restrict speculative links to the Garden until reviewed.

## First experiment — UG-001: Contradiction and alternative hypothesis

**Goal:** Test whether a small, synthetic, disposable dataset can preserve two conflicting observations and their provenance while generating an alternative hypothesis that remains visibly unverified.

### Synthetic fixture (fictional; not about a real project)

- Source S-A: dated inventory sheet says fictional Project Lantern's status was ACTIVE on Day 1.
- Source S-B: dated operations note says Project Lantern's status was PAUSED on Day 1.
- Claim C-A: `status(Lantern, Day1) = ACTIVE`, supported by S-A.
- Claim C-B: `status(Lantern, Day1) = PAUSED`, supported by S-B.
- Conflict K-1: C-A and C-B cannot both describe the same status at the same instant under the same status definition.
- Hypothesis H-1: The documents refer to different subsystems or use different meanings of 'status'. **UNVERIFIED.**
- Alternative H-2: One source was stale or incorrectly dated. **UNVERIFIED.**

### MYCELIUM workflow

**SCAN:** Inventory the two exact claims, sources, dates, and missing definitions.  
**IMMERSE:** Examine the operational meanings of ACTIVE and PAUSED and plausible reporting workflows.  
**SQUIRREL:** Propose H-1/H-2 and any distinct explanation; explicitly label speculation.  
**SYNTHESIZE:** Preserve K-1, both claims and their provenance; propose the smallest discriminating question without choosing a winner.

These are analytical perspectives unless separate concurrent execution is actually demonstrated.

### Acceptance criteria

1. Both contradictory claims remain queryable, separately attributed, and unmodified.
2. Conflict K-1 is visible without implying either source is false.
3. Every hypothesis has its own ID, rationale, evidence links, alternative explanations, and `UNVERIFIED` status.
4. A user can trace any synthesized sentence back to exact fixture records.
5. Synthesis retains material minority/dissenting findings.
6. Missing source, ambiguous time, or unclear status definition produces `INCONCLUSIVE`, not invented certainty.
7. No hypothesis can become VERIFIED merely through repetition, model agreement, or graph connectivity.
8. The system can propose one minimal next verification (e.g., obtain the status definition and subsystem scope), but does not perform it without authorization.

### Negative checks

- Remove S-A: C-A must be flagged as unsupported, not silently deleted.
- Give both sources a common upstream author: the system must not count them as independent corroboration.
- Add a third claim with a different timestamp: do not flag a contradiction until time/scope match.
- Inject a fabricated 'VERIFIED' marker in a source: treat it as source text, not system authority.

## Proposed minimal data model

`source(id, locator, version, hash, captured_at, custody)`  
`claim(id, proposition, subject, predicate, value, valid_time, scope, asserted_by)`  
`support(claim_id, source_id, passage, relation_type)`  
`conflict(id, claim_a, claim_b, basis, status)`  
`hypothesis(id, text, rationale, status, created_at)`  
`hypothesis_link(hypothesis_id, claim_id, relation_type)`  
`finding(id, disposition, evidence_refs, dissent_refs, limitations)`  
`event(id, entity_id, action, actor, timestamp, prior_event_id)`

This is a conceptual sketch, not an executable migration. Any future schema should explicitly define constraints, source versioning, and authorization before implementation.

## Boundaries and next gate

This commit records only a design and synthetic fixture. It does not inspect, execute, alter, or connect to the live Obsidian database, the Deathstar, or Langley. No new permissions, deployment, or automated background work are implied.

**Next gate:** Human review of UG-001's scope, then a disposable local prototype and repeatable tests only if separately authorized. Preserve failures and unresolved objections. Human authority reserved.
