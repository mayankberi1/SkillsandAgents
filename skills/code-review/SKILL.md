---
name: code-review
description: "Independently review actual changes against requirements and design."
---

# code-review

## Activation and inputs

Independently review actual changes against requirements and design. Relevant roles: Code Reviewer, Architect. Inputs: Approved before/after file comparison and complete change inventory, design and test evidence. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Assess the shared human-friendly coding standard explicitly: understandable names, flow, responsibilities and accurate explanatory comments. Identify concrete readability problems and useful simpler alternatives without arbitrary style enforcement.

Reconcile the complete new/modified/deleted file inventory with actual files and approved before/after evidence; request missing comparisons from the user without operating source control. Read surrounding code and tests. Assess correctness, scope, architecture/dependency direction, SOLID, maintainability and missing verification. Distinguish confirmed defects from concerns. Report location, severity, evidence and recommended remediation; never silently edit.

## Outputs and boundaries

Review verdict, findings, reviewed scope and limitations. Include decisions, deliverable references, evidence, risks/blockers and next action. Mandatory code-simplification assessment complements review; security-privacy is independent.
