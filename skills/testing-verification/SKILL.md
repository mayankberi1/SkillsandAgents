---
name: testing-verification
description: "Independently verify acceptance, integration and failure behaviour."
---

# testing-verification

## Activation and inputs

Independently verify acceptance, integration and failure behaviour. Relevant roles: Tester, Developer, Code Reviewer, Security Reviewer. Inputs: Acceptance criteria, actual changes and authorised test environment. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Derive risk-based cases from requirements independently of implementation claims. Exercise applicable unit/integration/regression/negative and critical E2E paths; reuse existing data/tools. Include lint/type/security checks when applicable. Record exact command/environment/result and map evidence to criterion IDs. Mocks do not establish integration. Do not rerun flaky failures until green; diagnose or escalate.

## Outputs and boundaries

Passed/Failed/Not run/Blocked/Not verified evidence and gaps. Include decisions, deliverable references, evidence, risks/blockers and next action. Does not replace code/security review; tests may write artifacts and need tool authorisation.
