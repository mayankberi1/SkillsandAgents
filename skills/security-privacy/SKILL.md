---
name: security-privacy
description: "Assess every changed file and relevant trust/privacy risks."
---

# security-privacy

## Activation and inputs

Assess every changed file and relevant trust/privacy risks. Relevant roles: Security Reviewer, Architect, Tester, Developer. Inputs: Complete changed-file inventory, threat context and approved scan evidence. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Reconcile the complete new/modified/deleted file inventory with actual files and approved before/after evidence; report missing baselines rather than certifying an incomplete comparison. Inspect every file, including docs/agent/skill/command/config. Review input trust, auth/authz, secrets, logs, dependency/config risks and sensitive data. Use approved scans when available; report missing tools. Apply threat/privacy modelling where risk warrants. Assign each file Pass/Fail/Not Applicable/Not Verified with rationale; findings Critical/High/Medium/Low. Block critical/material high; require independent re-verification of their fixes and meaningful remediation tests or explicit exceptions.

## Outputs and boundaries

Per-file assessment, findings, evidence, limits and blocking/exception decisions. Include decisions, deliverable references, evidence, risks/blockers and next action. dependency-assessment informs dependency risk; prompt instructions are not deterministic security.
