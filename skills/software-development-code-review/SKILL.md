---
name: software-development-code-review
description: "Review actual changes against requirements and design."
---

# software-development-code-review

## Activation and inputs

Review actual changes against requirements and design. Inputs: Approved before/after file comparison and complete change inventory, design and test evidence. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Assess the shared coding standard explicitly: shortest complete change, reuse of existing code, clear names and flow, focused responsibilities, pragmatic SOLID use, and comments only where needed. Identify unrequested features, dependencies, abstractions, wrappers, options, configuration, boilerplate, weak edge-case handling and concrete readability problems. Recommend simpler alternatives without arbitrary style enforcement.

Reconcile the complete new/modified/deleted file inventory with actual files and approved before/after evidence; request missing comparisons from the user without operating source control. Read surrounding code and tests. Assess correctness, scope, architecture and dependency direction, SOLID, maintainability and missing verification. Distinguish confirmed defects from concerns. Report location, severity, evidence and recommended remediation; never silently edit.

## Outputs and boundaries

Report the review result, findings, reviewed scope, limits, evidence, risks, blockers and next step. After coding, run this review automatically with testing, security review and simplification review. Run the checks in parallel when possible. Do not wait for user approval to start them.
Before you write any direct response to me, ensure it is written in ASD-STE100 Simplified Technical English, do not use techno-babble of any kind, do not physicalize things, always use the simplest turn of phrase, no need for synonymous phrases for variety, and use active voice.
Be concise and minimalist.
