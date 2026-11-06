# BL-009 step 1 — Coordinator checklist

Assignment COORD-DEV-TAG-IT1 r1. Backlog revision 8; BL-009 scope revision 2. Execution mode queue; active item BL-009, rank 2; queue revision 8. Requirements APR-ING-REQ-006, architecture APR-ING-ARCH-003 and design APR-ING-DES-005 are approved. Step 1 approved as APR-TAG-IT1-001. This assignment excludes updating user histories and step 2.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| CO1 | Approval and baseline | Record exact step scope; inspect current code/test inventory | Done | Approval is in [implementation plan revision 2](bank-tagging-iterations.md); six changed files are listed in the Developer plan | — |
| CO2 | Developer checkpoint | Obtain and save Developer's file checklist before source work | Done | Developer returned initial checklist; Coordinator saved [Developer plan](bank-tagging-step-1-developer-plan.md) and fixed the remaining field and approval details | Checklist acknowledged; proceed with source work |
| CO3 | Implementation checks | Reconcile Developer and Tester results against TAG-001, 002, 007–010 and the approved design | Done | Tester: 97 focused tests and 70 subtests passed; compile passed. Wider ingestion tests: 118 passed, 12 failed because `defusedxml` is absent. Code review passed. Security review passed for current code and tests after these record fixes. Ruff and full-repository tests remain unavailable. | No saved history was opened or changed |
| CO4 | Completion or blocker | Save step result and next approval state | Done | Step 1 is complete under APR-TAG-IT1-001. Independent test, code and security reviews passed. Step 2 needs separate approval. No saved history was opened or changed. Local storage has no encryption at rest; resolve this limit before storing real financial data. | Await step 2 approval; resolve storage choice before real data use |

No source change has been made by the Coordinator. No real saved history may be updated under this approval.

## Account-deletion decision

This detail follows the approved design and does not change step scope. During account-deletion review, list every same-currency rule that applies to all accounts in the history. Ask the user to choose keep or remove for each listed rule. Require the same reviewed rule IDs and choices when deletion runs. If the rules or choices have changed, stop and show a new review. Remove account-specific rules with the account. Full-history deletion removes all rules.

## Inventory update

The Developer found one additional test file during the baseline check: `tests/bank_statement_ingestion/test_distribution.py` expects the helper version and database format to match. Step 1 changes the database format only, so the test assertion now checks helper version 1 and database format 2. This is a test-only addition within the approved format update; include it in independent reviews.

## Independent Tester checkpoint

Saved [Tester checklist](bank-tagging-step-1-tester-plan.md), TEST-TAG-IT1 r1. The independent run confirmed 97 focused tests and 70 subtests passed, and compile passed. The broader suite has 12 failures because `defusedxml` is absent. No dependency was installed and no saved history was used.

## Independent Code Reviewer checkpoint

Saved [Code Reviewer checklist](bank-tagging-step-1-code-reviewer-plan.md), REVIEW-TAG-IT1 r1. The reviewer passed all six implementation files and the approved requirements, design and iteration plan. No actionable defect was found. The reviewer did not run tests. Five files have before/after hashes; `test_distribution.py` has no before hash, but its earlier assertion is recorded in the Developer plan.

## Independent Security Reviewer checkpoint

Saved [Security Reviewer checklist](bank-tagging-step-1-security-reviewer-plan.md), SEC-TAG-IT1 r1. The reviewer passed all six implementation files. The reviewer found no unsafe external call or change to financial fields. The review covers current content; the full before/after comparison is limited because `test_distribution.py` has no baseline hash. Local history has no encryption at rest; record this as a known storage limit. The reviewer did not run tests or open saved history.

## Security-review record fixes

The reviewer found stale Coordinator, lifecycle and backlog text. This checklist now lists six changed files and current test/review results. The lifecycle and backlog now state that implementation and reviews are complete. These are record fixes only; no source code or user history changed.
