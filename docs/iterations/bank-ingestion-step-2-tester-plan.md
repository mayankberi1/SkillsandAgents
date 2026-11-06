# BL-001 step 2 — Independent test checklist

TEST-BANK-002 r1. Scope 8, queue 8. Approval APR-ING-IT2-001. Requirements 4, architecture 2, design 4 and iteration plan 2 apply. Developer files must be frozen before testing.

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| T1 | Check scope, actual inventory, rules and test environment | Done | Approved step 2 only; five actual hashes match final Developer manifest |
| T2 | Run scoped suite and independent /tmp probes | Done | 70 tests/46 subtests and earlier seven probes pass; two new date-role probes fail |
| T3 | Reconcile coverage/docs and return evidence | Done | Failed P1 date-cell meaning check; actual commands and limits recorded below |

Source/test inventory: skills/bank-statement-ingestion/scripts/bank_history.py and statement_reader.py; tests/bank_statement_ingestion/test_bank_history.py, test_statement_reader.py and test_import_files.py. Check temporary installed copies through module calls; do not invoke a skill from source. Extra probes stay in /tmp. No project edits, setup changes or artifact delivery in this assignment. Use prepared /tmp/bank-step2-reader-env where required; independently check missing-protection behaviour with normal Python. Current step 2 records and approval states also require reconciliation; exclude unrelated changes.

## TEST-BANK-002 r1 — Failed

P1 at bank_history.py:729 (before repair): date proof checks values but not column meaning. One XLSX Date cell linked to both dates creates an absent posting date; a Posting date cell linked as transaction date creates an absent transaction date. Both incorrectly return imported/added=1/unresolved=0 and complete coverage. /tmp/test_bank_step2_independent.py reports two failures and one pass. Required: source-role checks, no dual meaning without explicit evidence, uncertain dates held with no false complete coverage, both regressions.

Independent prepared suite: 70 tests and 46 subtests pass. Seven earlier probes, real PDF/CSV/XLSX import/repeat/cleanup and all five compilation checks pass. Actual hashes match manifest. Normal Python without protection returns unsupported for XLSX and leaves CSV usable. All ING-010-A–N regressions covered. Commands use PYTHONPATH=/usr/lib/python3/dist-packages and /tmp/bank-step2-reader-env/bin/python for pytest tests/bank_statement_ingestion and /tmp/test_bank_step2_independent.py, /tmp/test_bank_independent.py, /tmp/test_bank_reviewer_independent.py. No project edits/setup changes.

Limits: count/size tests use reduced limits, not every maximum-size stress case. Network checks block Python sockets and inspect reader paths; no host-wide network isolation claim. ruff unavailable. Normal user setup and step 3 not verified. Failed evidence must remain after repair.

## TEST-BANK-002 r2 — date-role repair retest

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| V1 | Inspect exact repair and rerun failed date-role checks | Done | Both failures now pass; all 90 diff lines match actual before/current files |
| V2 | Verify valid separate dates and rerun scoped suite/earlier probes | Done | 73 tests/46 subtests, earlier seven probes and valid separate-date cases pass |
| V3 | Compile, confirm actual hashes/coverage and report limits | Done | Five files compile and match final manifest; reduced-limit/no-host-isolation/ruff limits retained |

Coordinator saved this retest checklist before execution. Source frozen at Developer r2 final hashes; earlier failed evidence remains above.

Final TEST-BANK-002 r2 result: Passed for date-role repair and step 2 test scope. Distinct transaction/posting cells with different dates work; missing posting date stays unknown; generic Date proposed as posting stays unresolved with no coverage. Actual evidence checks and 90-line repair inspected. Commands: prepared interpreter with PYTHONPATH=/usr/lib/python3/dist-packages ran /tmp/test_bank_step2_independent.py, /tmp/test_bank_step2_valid_dates.py, both earlier seven-probe files and pytest tests/bank_statement_ingestion; all five files compiled. No project edits or setup changes. Final five hashes match Developer r2 manifest/plan. Code and security reviews remain required. Size/count tests use reduced limits; network tests do not prove host isolation; ruff missing; normal user setup and step 3 not verified.

## TEST-BANK-002 r3 — code-review artifacts

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| A1 | Check frozen manifest/baselines and actual five source hashes | Done | Actual hashes and captured/recovered baselines checked |
| A2 | Send complete remaining records or verified full comparisons | Done | All 12 assigned records supplied |
| A3 | Reconcile delivery with Developer and report gaps | Done | No missing assigned record; Developer supplied other seven; current plan hashes disclosed |

Developer supplies five source/test files and two review policies; Tester supplies the remaining corpus. Missing before copies must be disclosed; verified recovery is allowed only when bytes match a previously independently recorded actual-file hash. Current file content is not proof of an unseen original comparison. Source remains frozen.

Final TEST-BANK-002 r3: All 12 assigned records delivered as complete files or checked complete comparisons. All five actual source/test hashes match the frozen list. Recovered backlog and lifecycle copies match earlier whole-file hashes. Their comparisons include step 1 closure and step 2 changes. Design and iteration comparisons match actual files. Current tester/reviewer plans supplied. Two copy errors were explicitly corrected. No tests, setup or project edits in this batch.

The Tester also checked the complete 292-line source comparison against captured step 1 files and current files. SHA256: `9efa72ec4053b3e09ed10ea1c37d1debda93c94bdedff854c55f47719b8295ae`. It matches byte for byte.

## TEST-BANK-002 r4 — security review artifacts

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| S-A1 | Check current inventory, policies/plans and frozen source hashes | Done | 20 files: 14 changed, six context. Five source hashes and source comparison unchanged |
| S-A2 | Supply complete context/plans and checked document comparisons | Pending | Include changed Coordinator, code reviewer and new security reviewer plans |
| S-A3 | Reconcile delivery, hashes and missing evidence | Pending | Final list and limits; no project edits, tests or setup |

Initial r4 plan saved. Developer owns five source/test files and two security policies. Tester must wait for acknowledgement before delivery.

First r4 checkpoint: Complete AGENTS and agent-planning texts and current 20-file list supplied. No removals. Current plans captured; approved core records and checked document comparisons are next. No edits, tests or setup.
