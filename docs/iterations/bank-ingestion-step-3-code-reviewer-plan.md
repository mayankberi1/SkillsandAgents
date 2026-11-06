# BL-001 step 3 — Independent code review checklist

Assignment REVIEW-BANK-003 r1. Scope 8, queue 8. Approval APR-ING-IT3-001. Developer reports frozen six-file diff and independent tests of the current combined helper.

| Task ID | File / criterion | Planned action | Status | Result / evidence / next action |
|---|---|---|---|---|
| R1 | Rules, approved inputs and actual inventory | Read review/simplification skills, requirements, design and full diff | Pending | — |
| R2 | `bank_history.py` | Review correctness, data links, correction, recovery and deletion safety | Pending | — |
| R3 | `test_maintenance.py`, `test_distribution.py` | Review meaningful acceptance and failure coverage | Pending | — |
| R4 | `SKILL.md`, `README.md`, `skills/CATALOG.md` | Review instructions and claims against actual behavior | Pending | — |
| R5 | Full changed-file inventory | Check scope, simplicity, changed records and final evidence | Pending | — |

Changed paths: six from `/tmp/bank-step3-final-manifest.json`. `test_bank_history.py` and `test_import_files.py` are unchanged but remain test context. Code reviewer must inspect the actual full files and complete diff; disclose any supplied-artifact or local-reader limit. No edits or tests. Step 2 reviews applied only to its frozen source; current combined source needs review.

Initial plan saved. Wait for Coordinator acknowledgement before review.

## R1 scope checkpoint

Reviewer read requirements 4, architecture 2, design 4, iteration plan 2 and the Developer/Tester plans. Manifest and diff headers match: six changed paths and two unchanged tests. The iteration row names the unchanged tests as part of step 3; Reviewer will check whether new maintenance tests cover their required behavior. Design 4 had stale status text showing step 3 unapproved. Coordinator updated the status and implementation evidence paragraph on 4 November. The current design diff must be included in the final documentation reconciliation. No source behavior reviewed yet.

## Source review checkpoint — possible P2

Reviewer has not found a P1 issue so far. A likely P2 issue remains under review: `apply_correction` appears to remove all verified periods for each linked statement for every correction. A description-only or amount-only correction may therefore create a coverage gap. Approved design and skill text appear to limit coverage removal to changes in source, account or date range. Reviewer is checking tests and related replacement/deletion behavior before confirming the finding. No edit or test was made.

## REVIEW-BANK-003 r1 final — Changes Requested

Reviewer checked current hashes for all six changed files and both unchanged tests against the final manifest. The reviewed files match the supplied diff. Three P2 findings; no P1. Stop for Developer repairs and new tests, then review the actual changed files again.

| Finding | File / location | Required correction |
|---|---|---|
| P2-1 | `bank_history.py` around lines 891–894 and 937–940 | `apply_correction` clears all linked verified periods for every field. Description/amount changes must not create false coverage gaps. Invalidate coverage only when the corrected source, account or date boundary affects it. Add a description-only correction test. |
| P2-2 | `bank_history.py` around lines 1203–1210 | `correct_history` copies a new source before processing. On unresolved input, the database rolls back but the copied file remains untracked. Remove it on rollback or track it with a visible retry result. Add a failure-path assertion. |
| P2-3 | `bank_history.py` around lines 1041–1057 | `_deletion_scope` loads all evidence and scans statement records once per transaction, causing O(transactions × records) work and runs at least twice per deletion. Build an index once or use scoped queries while preserving preview/recheck behavior. |

Tester evidence: focused 42 tests/15 subtests; full suite 115/61; compile passed. System Python lacked defusedxml and failed 12 XLSX tests; this limit is recorded. Reviewer ran no tests. Separate security review remains.

Review coverage includes helper changes, all step 3 tests, skill, README/catalogue, and approved requirements/design/iteration scope. Setup, prepared interpreter and POSIX limits are stated correctly. Simplicity is acceptable except for the quadratic deletion scan. No new dependency or production module.

## REVIEW-BANK-003 r2 — repair delta re-review

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| F1 | Check coverage invalidation fix and test | Done | Resolved; only account/card/date/posting-date changes invalidate |
| F2 | Check copied-source cleanup after rollback and test | Done | Resolved; cleanup or clear retained-path error, both tested |
| F3 | Check indexed deletion support lookup and test | Done | Resolved; one transaction-to-record index replaces repeated scans |
| F4 | Reconcile actual delta and return verdict | Done | R2 Pass; actual 3-file diff and hashes checked |

R2 re-review plan saved. Wait for Coordinator acknowledgement before delta review. No edits or tests.

Reviewer acknowledged R2 before inspecting the repair. All three findings remain open until independently checked.

REVIEW-BANK-003 r2 final: Pass. All three P2 findings are resolved. Deletion still loads all history into memory, so memory use grows with saved data; this is recorded as a limitation, not a blocking finding. Reviewer ran no tests. Tester reports 118 tests/61 subtests and compilation pass. No new blocking findings.

## REVIEW-BANK-003 r3 — security repair delta

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| G1 | Review safe stored-path and deletion checks | Done | Pass; hashes, basenames, containment, symlinks and file type checked |
| G2 | Review existing-history permission checks | Done | Pass; owner-only POSIX checks and fail-closed unsupported hosts |
| G3 | Review account-specific read filtering | Changes Requested | Account reassignment correction event is hidden from old account's view |
| G4 | Review fixture-only adjustments and full scope | Done | Pass; chmod changes affect synthetic test files only |
| G5 | Return delta verdict | Done | Changes Requested; one new P2 remains |

Initial r3 delta plan saved. Wait for Coordinator acknowledgement before re-review. No edits or tests.

Reviewer acknowledged R3 before inspection. G1–G5 remain open pending actual delta review.

R3 progress checkpoint: Delta hash matches. Reviewer confirmed stored hash/path validation before reads or deletion, POSIX permission checks for existing history/database/source folder/source files with fail-closed behavior, and that fixture chmod changes apply only to synthetic test files. The account-filter regression checks source name and correction evidence across two accounts. Reviewer is checking account-reassignment correction visibility before closing G3. No new finding so far.

R3 progress checkpoint — possible new P2: When a transaction moves from account A to B, the correction event is linked by transaction ID. `read_history(account_id=A)` finds the old source record ID but does not add the linked transaction ID to relevant changes; account A's view can omit the correction that explains removal. Current reassignment test checks only unfiltered history. Reviewer is confirming the complete delta and final disposition. No edits or tests.

REVIEW-BANK-003 r3 final: Changes Requested. The three prior security findings are resolved. One new P2 remains: a correction that moves a transaction from account A to B is hidden from account A's `read_history` output because the filter adds the source record ID but not the related transaction ID. Add a test for both account views after reassignment and retain isolation of unrelated evidence. Reviewer ran no tests; independent Tester reports full 121 tests/67 subtests and compile pass.

## REVIEW-BANK-003 r4 — account-reassignment delta

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| H1 | Check old/new account correction visibility | Done | Correction visible to accounts named in saved old/new account data |
| H2 | Check unrelated account isolation | Done | Third account cannot see correction evidence or source file |
| H3 | Reconcile actual two-file delta and tests | Done | Hash matches; Tester r4 full 122/69 and compile pass |
| H4 | Return final verdict | Done | Pass; no new blocking findings |

Initial r4 review checklist saved. Wait for Coordinator acknowledgement before delta review.

Reviewer read the R4 checklist and has not inspected the repair. Coordinator acknowledgement is recorded before the review starts.

R4 progress: Reviewer confirmed correction events use the saved old/new account IDs. The added test checks accounts A and B, an unrelated third account, and move-back history. Test limits and final disposition remain.

REVIEW-BANK-003 r4 final: Pass. The account reassignment finding is fixed. The code filter includes changes when the selected account appears in saved old/new account data. Tests check both affected accounts, a third unrelated account, and a move back. The delta hash matches. Reviewer ran no tests; Tester reports 122 tests/69 subtests and compile pass. No new blocking findings; r1–r3 findings remain in history.
