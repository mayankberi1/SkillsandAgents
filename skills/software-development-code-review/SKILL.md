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

Review verdict, findings, reviewed scope and limitations. Include decisions, deliverable references, evidence, risks/blockers and next action. Run software-development-code-simplification and software-development-security as separate checks in the main chat. State that these checks are not independent reviews.
