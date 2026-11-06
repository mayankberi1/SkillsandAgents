# Bank statement format revision 2 — Code reviewer checklist

Assignment REVIEW-BANK-FMT-002 r1. Backlog BL-001, scope revision 9, implementation review. Approval APR-ING-IT4-001. Read-only review of the six approved code, skill and test paths. Baseline and implementation hashes are listed in [the developer plan](bank-statement-format-r2-developer-plan.md).

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| CR-001 | Six approved files and current hashes | Reconcile actual paths and hashes with developer plan | Done | All six current hashes match the latest Developer plan. | Recheck after fixes. |
| CR-002 | `bank_history.py` | Review conversion, error structure, transaction boundary, evidence, source/sign checks, correctness and simplicity | Done | Needs changes: High amount-format evidence gap; Medium Excel epoch mismatch risk; Low date error may point to amount cell. Strict conversion and pre-write failure behavior otherwise align. | Re-review repaired code. |
| CR-003 | `SKILL.md` | Review accepted format instructions, examples and retained protections | Done | Needs changes: does not require evidence or user confirmation for unclear amount separator meaning. Other format and retry instructions are clear. | Re-review after update. |
| CR-004 | Four assigned test files | Review coverage against approved criteria and failure behavior | Done | Needs changes: posting-date overlap test omits raw date and format, so it stops before overlap logic. Other reviewed test paths pass; ambiguity and wrong-epoch tests are needed. | Re-review repaired coverage. |
| CR-005 | Cross-file scope and code quality | Check design coverage, unnecessary complexity and unapproved changes | Done | No extra dependency or unnecessary layer. Several redundant checks noted as low priority. Test paths are ignored by Git, which risks omission from delivery. | Reconcile test tracking before completion. |
| CR-006 | Review result | Record per-file verdicts, severity/location of findings and limits | Done | Overall verdict: Needs changes. Four test paths are ignored. Reviewer did not rerun tests or `git diff --check`; Ruff unavailable; no original source copy for byte-level comparison. | Re-review after fixes and confirm test delivery. |

## Initial checkpoint

The reviewer read the agent-planning and code-review instructions and the approved Developer plan. The initial checklist was acknowledged. The review found the issues recorded above. The Developer has already fixed the separator validation and date pattern length issues from the separate Security Reviewer. Remaining fixes and the amount-evidence design decision are in progress. Preserve this review result and append a new review checkpoint after repairs.
