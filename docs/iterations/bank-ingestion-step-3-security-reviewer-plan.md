# BL-001 step 3 — Independent security review checklist

Assignment SEC-BANK-003 r1. Scope 8, queue 8. Approval APR-ING-IT3-001. Actual combined source was tested with 118 tests/61 subtests and passed code review after three P2 repairs.

## Changed implementation and test files

| Task ID | File | Status | Required review |
|---|---|---|---|
| S1 | `skills/bank-statement-ingestion/scripts/bank_history.py` | Pending | Data privacy, paths, corrections, replacement, export/restore, deletion, transactions and source links |
| S2 | `tests/bank_statement_ingestion/test_maintenance.py` | Pending | Synthetic data, destructive behavior and cleanup checks |
| S3 | `tests/bank_statement_ingestion/test_distribution.py` | Pending | Temporary install, network guard, setup and cleanup |
| S4 | `skills/bank-statement-ingestion/SKILL.md` | Pending | User permissions, privacy, install/read behavior, limits and recovery instructions |
| S5 | `README.md` | Pending | Claims, setup and links |
| S6 | `skills/CATALOG.md` | Pending | Trigger and capability claims |
| S7 | `tests/bank_statement_ingestion/test_bank_history.py` | Pending | Unchanged relevant test context |
| S8 | `tests/bank_statement_ingestion/test_import_files.py` | Pending | Unchanged relevant test context |
| S9 | `skills/bank-statement-ingestion/scripts/statement_reader.py` | Pending | Unchanged reader and protection context |

## Changed records and checks

| Task ID | File / check | Status | Required review |
|---|---|---|---|
| D1 | `docs/product-backlog.md` | Pending | Approval, scope and status claims |
| D2 | `docs/iterations/bank-ingestion-iterations.md` | Pending | Approval history and step state |
| D3 | `docs/iterations/bank-ingestion-lifecycle.md` | Pending | Retained failures, approvals and evidence |
| D4 | `docs/iterations/bank-ingestion-solution.md` | Pending | Current design status and security claims |
| D5 | `docs/iterations/bank-ingestion-step-2-coordinator-plan.md` | Pending | Step 2 blocked recheck and step 3 authorization |
| D6 | `docs/iterations/bank-ingestion-step-2-developer-plan.md` | Pending | Evidence and artifact claims |
| D7 | `docs/iterations/bank-ingestion-step-2-tester-plan.md` | Pending | Test/review handoffs and limits |
| D8 | `docs/iterations/bank-ingestion-step-2-code-reviewer-plan.md` | Pending | Historical step 2 verdict scope |
| D9 | `docs/iterations/bank-ingestion-step-2-security-reviewer-plan.md` | Pending | Historical pass and failed recheck retained |
| D10 | `docs/iterations/bank-ingestion-step-3-product-owner-plan.md` | Pending | User approval and approved scope |
| D11 | `docs/iterations/bank-ingestion-step-3-developer-plan.md` | Pending | Current changes, tests, findings and limits |
| D12 | `docs/iterations/bank-ingestion-step-3-coordinator-plan.md` | Pending | Current stage and evidence |
| D13 | `docs/iterations/bank-ingestion-step-3-tester-plan.md` | Pending | Independent test evidence and limits |
| D14 | `docs/iterations/bank-ingestion-step-3-code-reviewer-plan.md` | Pending | Review findings and repairs |
| D15 | `docs/iterations/bank-ingestion-step-3-security-reviewer-plan.md` | Pending | This assignment record |
| C1 | Current changed-file inventory and actual hashes | Pending | Reconcile all paths, before/after comparisons, additions/removals |
| C2 | Cross-file risks and acceptance | Pending | Original copies, logs, rollback, shared data, account/card periods |
| C3 | Test evidence limits | Pending | Prepared dependency environment; system Python missing defusedxml; no host isolation, Ruff or real-user setup claim |

Review actual files and complete diffs with permitted tools. Do not edit or run tests. For each file, report Pass, Fail, Not Applicable or Not Verified with evidence. Preserve the earlier step 2 date-role failure and current-source mismatch history; step 2 review evidence applies only to its frozen source. No real bank data was used. Do not claim full erasure where shared copies/backups remain. Step 3 is approved for development; BL-001 remains In Progress until this review and final record reconciliation pass.

Initial plan saved. Wait for Coordinator acknowledgement before review.

Initial checkpoint: Reviewer read this plan, repository AGENTS.md, security-privacy and agent-planning. It has not inspected implementation files, hashes or diffs. The per-file inventory and checks are clear. Coordinator acknowledgement is required before review.

## Actual inventory checkpoint

Reviewer checked the eight source/test paths against `/tmp/bank-step3-r2-final-manifest.json`; all current hashes match. That manifest covers six implementation/test changes and two unchanged context files. Git does not show `docs/` and `tests/` because `.gitignore` excludes them, so Git status alone is not the full record inventory.

Coordinator confirms these 15 documentation records changed or were created and are assigned in D1–D15 above: `docs/product-backlog.md`; `docs/iterations/bank-ingestion-iterations.md`, `bank-ingestion-lifecycle.md`, `bank-ingestion-solution.md`; `bank-ingestion-step-2-coordinator-plan.md`, `bank-ingestion-step-2-developer-plan.md`, `bank-ingestion-step-2-tester-plan.md`, `bank-ingestion-step-2-code-reviewer-plan.md`, `bank-ingestion-step-2-security-reviewer-plan.md`; `bank-ingestion-step-3-product-owner-plan.md`, `bank-ingestion-step-3-developer-plan.md`, `bank-ingestion-step-3-coordinator-plan.md`, `bank-ingestion-step-3-tester-plan.md`, `bank-ingestion-step-3-code-reviewer-plan.md`, `bank-ingestion-step-3-security-reviewer-plan.md`. No other documentation record was edited for this work. The reviewer has not started per-file assessment.

## Review progress checkpoint — possible privacy issues

Reviewer reconciled nine source/context files: six changed files match the frozen final manifest; the reader and two unchanged tests match baseline. Initial review of the helper, reader, skill and distribution test raised two possible privacy issues for confirmation: database permissions may not be checked before financial data is read or saved; and account-specific `read_history` may return source metadata plus all import/correction/replacement attempts. Reviewer is checking the rest of the files and records before confirming scope or severity. No final finding yet.

## Review progress checkpoint — confirmed privacy gaps; path check pending

Reviewer confirmed the database/source directory mode gap at helper lines 157–164 and 167–180: creation uses private modes, but existing/copied history modes are not checked before reads or writes. Reviewer also confirmed that `read_history(account_id=...)` filters account rows but returns all change attempts and source/file rows, including other accounts' source names and correction evidence. A possible higher-severity issue remains under review: deletion may use a database `content_hash` as a path without validating it when `copy_state` is not `ready`. The reviewer is checking the exact path flow and remaining records; no final verdict yet.

## Review progress checkpoint — confirmed P1 and P2 findings

Reviewer confirmed a High/P1 path issue: `delete_history` does not check the live history before deletion and unlinks `sources / row['content_hash']` without validating the value as a safe basename/hash. The SQLite field has no format check. A tampered/corrupt database can store `../outside-file`; a deletion request can then unlink a file outside the managed source directory. This requires a tampered/corrupt database and explicit deletion; normal statement imports calculate the hash themselves.

Two P2 privacy issues remain confirmed: existing history permissions are not checked before use, and account-specific history returns file/source rows and change attempts across accounts. The prior step 2 security record also incorrectly called the SQLite `mode=rw` connection read-only and claimed 0600 checks for all opens. Reviewer is completing remaining changed-diff/document coverage before final verdict.

## SEC-BANK-003 r1 final — Fail

All 24 assigned paths were reconciled: nine source/test/context files and 15 changed or new work records. Six implementation/test files match their manifest; three context files match baseline. Git omits documentation and test records because `.gitignore` excludes them. No other documentation records changed for this work. No real bank data was used.

| Finding | Severity | Required action |
|---|---|---|
| P1 | High | Before deletion, validate every stored content hash/path and confirm the resolved target stays inside the managed source folder. Add a malformed database test that proves an outside file stays. |
| P2 | Medium | Check existing history folder, database, source folder and source file permissions before use; fail safely or set private permissions. Add tests for each open-permission case. |
| P2 | Medium | When `read_history(account_id=...)` is used, return only source files and import/correction records linked to that account. Add a two-account test. |

Per-file verdicts: `bank_history.py` Fail; `test_maintenance.py` Fail (missing path and permission tests); `test_bank_history.py` Fail (missing permission tests); `step-2-security-reviewer-plan.md` Fail (inaccurate historical claims); this step 3 security plan Fail until this verdict is saved. `test_distribution.py`, `SKILL.md`, README, catalogue, import tests and statement reader Pass. Other listed records D1–D8 and D10–D14 Pass.

The step 2 security plan describes SQLite `mode=rw` as read-only and overstates permission checks. Keep the prior text as history and append a dated correction. This review did not run tests. Developer/Tester evidence: 118 tests/61 subtests passed. No real bank data; no Ruff, host-wide network isolation, real-user setup or full stress verification.

## SEC-BANK-003 r2 — re-review after repairs

Developer reports changes to `bank_history.py`, `test_maintenance.py`, `SKILL.md`, and `test_bank_history.py`. The repair adds stored-path validation, fail-closed existing-history permission checks, account-scoped source/change output, hostile-path tests, four permission tests and a two-account test. The earlier security failure remains until an independent re-review confirms these changes. Tester r3 independently reports five targeted tests/six subtests, focused 89/48, full 121/67, compilation pass, and actual four-path diff/hash match. No security verdict yet.

## SEC-BANK-003 r2.1 — final repair re-review

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| R1 | Recheck deletion path containment on actual current source | Pending | Corrupt database path cannot escape managed source folder |
| R2 | Recheck existing-history permission enforcement | Pending | History folder, database, source folder and source files; fail closed |
| R3 | Recheck account-scoped changes after reassignment | Pending | Old/new accounts see the event; unrelated account remains hidden |
| R4 | Recheck correction to historical security claims | Pending | Step 2 record correction retained; no current false claim |
| R5 | Reconcile actual current hashes, tests, code review and full record list | Pending | Latest manifest; code review r4 Pass; tester r4 full122/69 |
| R6 | Give final per-file security result | Pending | Pass/Fail/Not Verified for all changed security-relevant files and record delta |

Initial r2.1 checklist saved. Wait for Coordinator acknowledgement before re-review. No edits or tests.

Reviewer read the R2.1 checklist and will inspect only its listed repairs. No edits or tests. Coordinator acknowledgement is saved before re-review.

## R2.1 partial result and record correction

Reviewer rechecked R1–R3 and confirmed the path containment, owner-only permission checks, and account-scoped correction visibility pass. The reviewer found D9 still needed a dated follow-up that records the permission repair, and this plan needed a final R2.1 result. Coordinator appended the D9 follow-up above. R4–R6 remain open until the reviewer checks both records and reconciles the exact inventory. No final security verdict yet.

## SEC-BANK-003 r2.1 final result — security checks pass

The independent reviewer confirmed R1–R4 pass. The reviewer independently checked all eight r4 source/test manifest hashes and both unchanged context files. All 15 D1–D15 records exist. The reviewer confirmed the current contents of D9. All assigned source and test files, D1–D12 and D14 pass. D13 was initially marked Not Verified because this plan listed its own hash before the inventory was appended. The Tester has now stated this clearly: D13's listed hash is the pre-append hash, and its current contents were checked by the reviewer. D15 is this file; its hash in the inventory is also a pre-final-update value. Self-hashes cannot be current after the record changes. No other record has a hash mismatch. The reviewer did not run tests or edit files.

| Check | Result | Evidence |
|---|---|---|
| R1 stored path safety | Pass | Reviewer rechecked current code and hostile-path test evidence |
| R2 existing history permissions | Pass | Reviewer rechecked fail-closed checks; Tester reports four permission cases pass |
| R3 account-scoped correction history | Pass | Reviewer checked old/new account visibility and unrelated-account privacy |
| R4 correction to step 2 security record | Pass | D9 now records the historical error and repair accurately |
| R5 source and record inventory | Pass | Eight source/test hashes match; all 15 records exist; D13 and D15 self-hash limits are stated |
| R6 final per-file result | Pass | All assigned source/test files and planning records pass after the D13 clarification; D15 records this result |

Security review is Pass for the current Step 3 source and records. Preserve SEC-BANK-003 r1 Fail and the earlier re-review findings above as history. Test evidence remains the independent Tester result: 122 tests and 69 subtests passed; compile passed. Ruff was unavailable, host-wide network isolation was not verified, and tests used synthetic data only.

## Final status-record audit — 4 November 2026

After the completion update, the independent reviewer checked the current D1 backlog, D2 iteration record, D3 lifecycle, D4 design and D12 Coordinator plan. The reviewer found and reported stale BL-001 status and storage wording in D1. The Coordinator labeled earlier stages as historical, stated the selected SQLite and retained-copy choice, and linked current completion evidence. The reviewer rechecked the corrected D1 and confirmed it has no stale current-status or storage claim. The other four records agree on BL-001 Done, step 3 review/test results, queue 8 with no active item, and limits. D13/D15 state their own-hash limits. No tests or source edits were part of this document audit. Final record audit: Pass.

The reviewer also checked the final D1 sentence about design and tests. It matches design 4, implementation records and generated-data test evidence. It states that real statement layouts were not tested. No claim exceeds the recorded evidence.
