# BL-001 step 3 — Independent test checklist

Assignment TEST-BANK-003 r1. Scope 8, queue 8. Approval APR-ING-IT3-001. Developer reports a frozen six-file diff and 115 tests/61 subtests passing. Test the actual current files and all ING-001–014 acceptance checks.

| Task ID | Action | Status | Result / evidence / next action |
|---|---|---|---|
| T1 | Reconcile scope, actual file list, baseline and rules | Done | Eight actual hashes match the manifest: six changed paths, two unchanged tests. Approved requirements ING-001–014 and ING-010-A–N mapped. Tester read full assigned skills and Coordinator policy. |
| T2 | Independently test corrections, recovery, export, restore and deletion | Done | Focused synthetic tests: 42 passed, 15 subtests passed; no failures or edits |
| T3 | Check installed-copy behavior, instructions, catalogue and prior ingestion | Done | Temporary installed-copy smoke and setup/catalogue checks passed |
| T4 | Check full suite and failure evidence | Done | Prepared environment: 115 passed, 61 subtests; system Python failure retained; compilation passed |
| T5 | Return coverage, hashes, failures and verdict | Done | All eight actual hashes match; acceptance coverage/limits reported; no source edits |

Initial plan saved. Wait for Coordinator acknowledgement before test work. No user data, source edits, dependency setup or release work.

## T1 inventory checkpoint — before tests

Tester checked all eight actual paths against the final manifest. Six paths changed and two tests remain unchanged. The actual helper combines step 2 and step 3; earlier step 2 evidence does not cover the combined file. Test scope maps to all ING-001–014 and ING-010-A–N. The Tester read the full Tester and agent-planning skills and Coordinator policy. Next: independent synthetic maintenance/failure checks, installed-copy checks, full suite and compilation. No test has run in this assignment.

## Focused test checkpoint

Independent focused tests passed: 42 tests and 15 subtests. They cover synthetic corrections, source replacement, export, restore, deletion, coverage, buffer checks, installed-copy import, setup text and catalogue entry. No failures or edits. Full bank suite and compilation remain.

## Full-suite environment checkpoint

System `python3` lacks the protected XLSX library `defusedxml==0.7.1`. The suite had 12 reader/XLSX failures; 104 tests and 60 subtests passed. This matches the documented unsupported-dependency behavior, but it does not complete the required full-suite check. Compilation passed for all seven scoped Python files, and all eight actual manifest hashes still match. Rerun using the existing prepared step 2 interpreter and its recorded system XML path. No setup/download or source edits.

## Final TEST-BANK-003 r1 handoff

Focused tests passed: 42 tests and 15 subtests. Full suite in the existing prepared interpreter passed: 115 tests and 61 subtests. System Python failed 12 XLSX checks because `defusedxml==0.7.1` is absent; this earlier run is retained. Compilation passed for both scripts and all five bank test files. Temporary installed-copy CSV import/repeat and setup/catalogue checks passed. All eight actual manifest hashes still match. No source edits, real bank data, setup/download or normal user configuration changes.

Coverage maps to ING-001–014 and ING-010-A–N across ingestion, persistence, coverage, duplicates/retries, maintenance, hostile input and installed-copy checks. Fixtures are synthetic. Host-wide network isolation and real statement variants were not tested. Ruff is unavailable; no lint run. Independent code and security reviews remain required. The earlier step 2 date-role failure and retest history remains; current tests cover the combined helper.

## TEST-BANK-003 r2 — code review fixes

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| V1 | Check F1–F3 repair diff and actual file hashes | Done | Actual delta matches 216-line diff and r2 manifest; only three listed paths changed |
| V2 | Independently test the three repaired behaviors | Done | Four targeted F1–F3 regression checks passed; focused 45 tests/15 subtests pass |
| V3 | Rerun focused/full suite and compile; report limits | Pending | Developer reports 45/15 focused and 118/61 full |

Initial r2 checklist saved. Wait for Coordinator acknowledgement before independent retest. Do not edit source. Preserve r1 tests and system-Python dependency failure history.

R2 checkpoint: Tester checked actual before/after files against the complete repair diff and manifest. Only the three assigned paths changed. Four targeted regressions passed: coverage preservation, failed replacement cleanup and indexed deletion support. Focused suite passed with 45 tests and 15 subtests. No source defect found so far. Full suite, compile and final hash check remain. No edits.

## TEST-BANK-003 r3 — security repair retest

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| W1 | Reconcile security repair diff and four changed paths | Done | Actual four-path delta matches manifest and saved diff |
| W2 | Independently test traversal, permissions and account filtering | Done | Hostile paths, four permission targets, two-account filter and affected fixtures: 5 tests/6 subtests passed |
| W3 | Rerun focused/full bank tests and compilation | Done | Focused 89/48; full 121/67; compile passed |
| W4 | Report actual hashes, failures and limits | Done | Four hashes match; first two-fixture failure retained; synthetic-only limits reported |

Initial r3 checklist saved. Wait for Coordinator acknowledgement before independent testing.

R3 checkpoint: Actual four-path before/after diffs match the final diff and manifest. Targeted hostile-path, permission, two-account filtering and legacy fixture checks passed: five tests and six subtests. No source edits. Focused/full suites, compile and final hash check remain.

Final TEST-BANK-003 r3: Targeted security checks passed (5 tests/6 subtests). Focused history/maintenance/distribution passed (89/48). Full bank suite passed (121/67). Compilation passed for both scripts and all five bank test files. The actual four-path delta matches the diff and manifest. No source edits/setup changes. First full run with two old fixtures at broad modes is retained. Tests use synthetic data; host-wide network isolation and real bank statements were not tested. Ruff is unavailable. Independent code/security re-review remains.

## TEST-BANK-003 r4 — account reassignment

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| X1 | Reconcile r4 delta and actual hashes | Done | Actual two-file delta matches manifest and 52-line diff hash |
| X2 | Test both affected accounts, unrelated account and repeated reassignment | Done | Reassignment/move-back and unrelated-account checks: 2 tests/2 subtests pass |
| X3 | Run focused/full suite and compile | Done | Focused 49/23; broader 90/50; full 122/69; compile passed |
| X4 | Report final hashes, failures and limits | Done | Two-file delta/hashes match; failures/limits retained; no edits |

Initial r4 checklist saved. Wait for Coordinator acknowledgement before independent re-verification.

R4 checkpoint: Actual before/after files show only `bank_history.py` and `test_maintenance.py` changed. Their hashes match the r4 manifest and the complete 52-line diff hash matches. Tests for both affected accounts, move-back history and unrelated-account privacy passed: two tests and two subtests. Focused/full suite, compile and final hashes remain. No edits.

R4 focused checkpoint: Focused maintenance/distribution passed (49 tests/23 subtests). Broader history/maintenance/distribution passed (90/50). No failures or edits. Full bank suite, compilation and final hash reconciliation remain.

Final TEST-BANK-003 r4: Actual two-file delta matches saved diff and hashes. Reassignment and move-back checks passed. Focused maintenance/distribution 49 tests/23 subtests; broader history/maintenance/distribution 90/50; full bank suite 122/69. Compilation passed for both scripts and all five bank tests. Synthetic data only; no source/setup edits. Ruff unavailable and host-wide network isolation unverified. All earlier failures remain recorded. Independent code/security reviews remain required.

## TEST-BANK-003 r5 — final record inventory

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| Z1 | Reconcile every changed/created planning record | Done | All D1–D15 records exist; hashes are listed below |
| Z2 | Reconcile source/test file list and latest hashes | Done | All eight r4 manifest paths match; two unchanged context files match their saved step 2 hashes |
| Z3 | Return complete inventory and missing/conflicting records | Done | No missing or unexpected changed file; no edits/tests |

Initial r5 checklist saved. Wait for Coordinator acknowledgement before inventory checks.

Final TEST-BANK-003 r5 inventory: all 15 assigned records exist. The hashes below are the values checked before this inventory was appended. D13 is this file, so its listed hash is the pre-append value; a file cannot contain its own final hash. The reviewer checked D13 by reading its current contents. All eight paths in `/tmp/bank-step3-r4-full-manifest.json` match their recorded hashes. `statement_reader.py` and `test_statement_reader.py` remain unchanged at their saved step 2 hashes. No missing or unexpected changed file. No tests or source edits in r5.

| Record | SHA-256 |
|---|---|
| D1 `docs/product-backlog.md` | `a61cc071eb6482c13e7732e163e33aa24ee8ed5d42f29c06d9ce68fee61d345b` |
| D2 `docs/iterations/bank-ingestion-iterations.md` | `d043e9b552fba339a42ec19dff01ad5c1d89e6946aae8cdab8c9b3dbdcf0bae7` |
| D3 `docs/iterations/bank-ingestion-lifecycle.md` | `4c905c82397d5d5825c910f1723b991d67003b125107d48d24e0086824448e39` |
| D4 `docs/iterations/bank-ingestion-solution.md` | `0ba1df385b3ddf515b954a0decdeee138e24180e8feda53a089655ff37116d7e` |
| D5 `docs/iterations/bank-ingestion-step-2-coordinator-plan.md` | `edafc248965b08fbde4f429a29aebea2b3b920bfc787adec76fa549742ab9530` |
| D6 `docs/iterations/bank-ingestion-step-2-developer-plan.md` | `203a073881b3dea8a028de41c74ea2094772d4ae57a84110c627cc019a95cff5` |
| D7 `docs/iterations/bank-ingestion-step-2-tester-plan.md` | `58f0622d76d65592916f00f94a5471dd821c7d963eac1a1f1dcd4b22a0472c6e` |
| D8 `docs/iterations/bank-ingestion-step-2-code-reviewer-plan.md` | `f36c559325f264e7cb270ff14ef1586d95f0f9bae740b2d10b2d51886fac2399` |
| D9 `docs/iterations/bank-ingestion-step-2-security-reviewer-plan.md` | `57481747161ca56bdf693e9287cebcd22c27a791d045ba2d51be6e417da27c79` |
| D10 `docs/iterations/bank-ingestion-step-3-product-owner-plan.md` | `1c979e61af72967e36cda496702443aa89630455644949040c022d63c46e5678` |
| D11 `docs/iterations/bank-ingestion-step-3-developer-plan.md` | `cf78035e91f81b29127bd4ae9216890c7439cc6451b1e02c6002ed59558f8812` |
| D12 `docs/iterations/bank-ingestion-step-3-coordinator-plan.md` | `9d7fdad41c7edb8b89caaaa2ab04029670f661d35005c535f310ebce879154c8` |
| D13 `docs/iterations/bank-ingestion-step-3-tester-plan.md` | `7e51106ebd2336345c7bc4225ff57e70d82bcb26e98c3c29108aa6a10b3db141` |
| D14 `docs/iterations/bank-ingestion-step-3-code-reviewer-plan.md` | `b2e11bd04da7b185cb0f5b87d5850941833ccdedc6702e35e796888e149ed4a3` |
| D15 `docs/iterations/bank-ingestion-step-3-security-reviewer-plan.md` | `6da408090689b302c239441575d112d3c462529fb4ac9ceb77e98accd5adbadb` |
