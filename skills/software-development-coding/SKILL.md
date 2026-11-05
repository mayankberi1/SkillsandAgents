---
name: software-development-coding
description: "Write and test the smallest complete, readable change for an approved iteration."
---

# software-development-coding

## Activation and inputs

Write and test the smallest complete, readable change for an approved iteration. Inputs: approved iteration and design, affected files, actual file state.
Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Follow the shared coding standard in software-development-workflow. Before editing, ask about unresolved coding choices, show the affected files and detailed proposed changes, and wait for approval of the coding stage. Stop and ask the user to resolve a material design gap before implementing dependent behaviour.

Confirm authorisation and approved file baseline. Trace relevant code before editing. Select the smallest complete change that remains easy to read; write meaningful behavioural tests, using test-first reproduction for defects where feasible. Implement only after coding-stage approval. Run only approved checks. Inspect the diff for scope drift; reconcile docs and report evidence. Then present the next stage for approval. Do not describe main-chat checks as independent.

## Outputs and boundaries

Scoped diff, tests, evidence and handoff. Include decisions, deliverable references, evidence, risks/blockers and next action. software-development-debugging handles failed checks; software-development-code-simplification evaluates reduction.
