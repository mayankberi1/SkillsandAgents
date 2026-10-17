---
name: code-simplification
description: "Assess unnecessary complexity without weakening required behaviour."
---

# code-simplification

## Activation and inputs

Assess unnecessary complexity without weakening required behaviour. Relevant roles: Developer, Code Reviewer, Solution Designer. Inputs: Approved scope and actual implementation/design. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Perform this assessment each iteration. Look for unused layers, speculative interfaces/classes, duplication, unnecessary dependencies and indirect flows. Compare simpler alternatives against required correctness/security/accessibility/verification. Make only authorised minor in-scope reductions; propose larger changes. Re-run relevant tests for changed behaviour paths.

## Outputs and boundaries

Simplification assessment, justified exceptions and scoped proposals. Include decisions, deliverable references, evidence, risks/blockers and next action. Does not authorise cleanup or remove required safeguards.
