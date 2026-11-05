---
name: software-development-security
description: "Assess every changed file and relevant trust/privacy risks."
---

# software-development-security

## Activation and inputs

Assess every changed file and relevant trust/privacy risks. Inputs: Complete changed-file inventory, threat context and approved scan evidence. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Reconcile the complete new/modified/deleted file inventory with actual files and approved before/after evidence; report missing baselines rather than certifying an incomplete comparison. Inspect every file, including docs, skills, commands and configuration. Review input trust, access checks, secrets, logs, dependency/config risks and sensitive data. Use approved scans when available; report missing tools. Apply threat/privacy modelling where risk warrants. Assign each file Pass/Fail/Not Applicable/Not Verified with rationale; findings Critical/High/Medium/Low. Block critical/material high findings. After a fix, inspect the changed files and run meaningful checks again. Report this as a follow-up check by the main chat, not an independent review.

## Outputs and boundaries

Per-file assessment, findings, evidence, limits and blocking/exception decisions. Include decisions, deliverable references, evidence, risks/blockers and next action. software-development-dependencies informs dependency risk; prompt instructions are not deterministic security.
