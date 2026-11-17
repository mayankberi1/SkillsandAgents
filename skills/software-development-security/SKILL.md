---
name: software-development-security
description: "Assess every changed file and relevant trust/privacy risks."
---

# software-development-security

## Activation and inputs

Assess every changed file and relevant trust/privacy risks. Inputs: Complete changed-file inventory, threat context and approved scan evidence. Read applicable central AGENTS.md; this capability grants no additional authorisation.

After coding, run this review automatically with testing, code review and simplification review. Run the checks in parallel when possible. Do not wait for user approval to start them.

## Procedure

Reconcile the complete new/modified/deleted file inventory with actual files and approved before/after evidence; report missing baselines rather than certifying an incomplete comparison. Inspect every file, including docs, skills, commands and configuration. Review input trust, access checks, secrets, logs, dependency/config risks and sensitive data. Use approved scans when available; report missing tools. Apply threat/privacy modelling where risk warrants. Assign each file Pass/Fail/Not Applicable/Not Verified with rationale; findings Critical/High/Medium/Low. Block critical/material high findings. After a fix, inspect the changed files and run meaningful checks again. Report this as a follow-up check by the main chat, not an independent review.

## Outputs and boundaries

Per-file assessment, findings, evidence, limits and blocking/exception decisions. Include decisions, deliverable references, evidence, risks/blockers and next action. software-development-dependencies informs dependency risk; prompt instructions are not deterministic security.
Before you write any direct response to me, ensure it is written in ASD-STE100 Simplified Technical English, do not use techno-babble of any kind, do not physicalize things, always use the simplest turn of phrase, no need for synonymous phrases for variety, and use active voice.
Be concise and minimalist.
