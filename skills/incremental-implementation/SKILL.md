---
name: incremental-implementation
description: "Implement an approved iteration with small scoped tested changes."
---

# incremental-implementation

## Activation and inputs

Implement an approved iteration with small scoped tested changes. Relevant role: Developer. Coordinator delegates this work and may read the output contract, but must not execute its source-change procedure. Inputs: Approved iteration/design, affected files, actual file state. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Apply the shared human-friendly coding standard. Prefer descriptive names, cohesive functions and straightforward control flow; explain non-obvious reasons and avoid clever compression. Resolve material design gaps through Coordinator before implementing dependent behaviour.

Confirm authorisation and approved file baseline. Trace relevant code before editing. Select the smallest complete change; write meaningful behavioural tests, using test-first reproduction for defects where feasible. Implement and run appropriate checks. Inspect diff for scope/drift; reconcile docs and report evidence. Send to independent reviews rather than self-certifying completion.

## Outputs and boundaries

Scoped diff, tests, evidence and handoff. Include decisions, deliverable references, evidence, risks/blockers and next action. debugging-recovery handles failed checks; code-simplification evaluates reduction.
