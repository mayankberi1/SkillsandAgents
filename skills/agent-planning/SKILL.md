---
name: agent-planning
description: "Create and maintain evidence-backed task checklists for each coding-agent assignment, with persistent Markdown checkpoints and coverage reconciliation."
---

# agent-planning

## Ownership and persistence

Every specialist owns its plan; Coordinator owns persistence and validates coverage. Use a separate flat Markdown record at `docs/iterations/<iteration-id>-<agent-id>-plan.md`, linked from the iteration record. Include the assignment ID/revision so repeated assignments do not overwrite earlier evidence. This is a work checklist, not a new approval or a separate workflow database. Follow central AGENTS.md and existing tool permissions.

Before substantive work, read the latest plan and supplied scope/baseline, then create or reconcile the checklist. Return the initial plan to Coordinator for recording and resume only from its acknowledged checkpoint. Specialists with denied edits must not write the record through shell or another tool. Coordinator persists updates with existing native permission requirements; if persistence is unavailable, report the checkpoint as unsaved and block dependent continuation. Do not claim an in-memory checklist or native todo list is durable storage.

## Plan contents

Record assignment, agent, scope revision, requirements/approval references, baseline/inventory references, dependencies, limitations and next action. Use stable task IDs and this table:

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| SEC-001 | src/example.ts | Review input validation and authorisation | Pending | — | Read approved file and comparison |

Statuses: Pending, In Progress, Done, Blocked, Not Applicable. Done means the planned action was performed, not that its result passed. Record failures explicitly. Not Applicable requires a reason; missing evidence is Blocked, not Not Applicable. Keep actual test results and security verdicts separate from task progress.

Build tasks from the complete assigned scope rather than only files already read. Code and security reviewers create a task for each new/modified/deleted file in the supplied inventory, plus applicable cross-file, design and verification checks. Deleted files require approved removal evidence. Security Reviewer records the required per-file Pass/Fail/Not Applicable/Not Verified verdict in the result column. Tester maps tasks to acceptance criteria and risk-based checks; other specialists map tasks to required decisions, deliverables and verification. Missing or unverifiable inventory remains an explicit blocker.

## Execution and checkpoints

Choose small coherent batches. Independent reads within a batch may run in parallel where supported; dependent actions remain sequential. Inspect every tool result and update the corresponding rows with actual file/location, comparison or test evidence. Never mark a task Done just because a read was scheduled.

Return updated rows after each batch, on a blocker, before a context/session transition, and at final handoff. Coordinator saves and acknowledges each checkpoint before the next batch is delegated. Include the plan path, assignment revision, completed and remaining task IDs, unsaved changes and next action. Preserve previous failures and re-verification attempts rather than replacing them with later success. Avoid secrets in records.

On resume, reconcile the saved plan with actual files, baseline, inventory and scope; In Progress tasks are unverified until checked. Follow the central resume confirmation policy. Changes invalidate affected completed results and require renewed verification and applicable approvals; retain earlier evidence.

## Completion check

Compare planned file paths and criteria against the supplied inventory and acceptance requirements. Account explicitly for missing, duplicate, newly discovered and removed items. No unqualified completion with Pending, In Progress or Blocked required tasks, missing per-file verdicts, or unsupported results. A completed review may still have a Fail verdict and blocking findings. Coordinator independently checks the coverage and evidence before accepting the handoff.

Include changed plan records in documentation reconciliation. Administrative status updates must cite existing evidence; new substantive claims or scope changes need applicable independent assessment. The checklist makes omissions visible; it does not guarantee complete analysis or replace independent review.
