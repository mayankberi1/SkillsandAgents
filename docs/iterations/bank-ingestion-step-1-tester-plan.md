# BL-001 step 1 — Independent test checklist

TEST-BANK-001 r1. Scope 8, queue 8. Approval APR-ING-IT1-001. Inputs: requirements 4, architecture 2, design 4 and iteration plan 2. No later step approval.

| Task ID | Deliverable | Action | Status | Evidence / next action |
|---|---|---|---|---|
| T1 | Rules and approvals | Read AGENTS and testing/planning skills; check current approvals | Done | APR-ING-IT1-001 covers step 1 only |
| T2 | Acceptance coverage | Map ING-010-A–N and step 1 requirements to checks | Done | A–M pass tested cases; N/header evidence has blocking defect |
| T3 | Two new source/test files | Run existing and independent focused checks, using /tmp for extra tests | Done | 33 existing tests pass; four independent checks fail; compilation passes |
| T4 | Changed planning records | Check current scope/approval consistency | Done | Backlog/lifecycle/iterations agree; design has two stale current-state statements |
| T5 | Handoff | Report passed/failed/not-run checks, evidence and limits | Done | Failed; four defects require fixes and independent recheck; ruff absent |

Inventory: skills/bank-statement-ingestion/scripts/bank_history.py; tests/bank_statement_ingestion/test_bank_history.py; docs/product-backlog.md; docs/iterations/bank-ingestion-solution.md, bank-ingestion-iterations.md, bank-ingestion-lifecycle.md, bank-ingestion-coordinator-plan.md, bank-ingestion-step-1-developer-plan.md, bank-ingestion-solution-designer-plan.md, bank-ingestion-iteration-product-owner-plan.md and this checklist. Coordinator persists all records. No source edits, Git operations or execution of the distributed skill from source.

Progress evidence: existing 33 tests pass independently. Four additional checks in /tmp/test_bank_independent.py found failures: P1 amount substring permits source -110.00 to support proposed +10.00; P1 complete='false' acts as true; P1 malformed header dates 2026-01-010 to 2026-01-310 support January 1–31 through substring matching; P2 one invalid record date rolls back valid rows in the same file. Independent result so far: three failures and one error. No project edits; final coverage check pending. Step 1 cannot pass until defects are fixed and independently rechecked.

Final TEST-BANK-001 r1 result: Failed. Reproductions at bank_history.py lines 461, 573, 124 and 447 respectively (line numbers before fixes). Require complete money/date evidence, true boolean type checks and unresolved handling of bad record dates without losing valid partial work. Existing unittest discovery passes 33 tests; four /tmp checks report three failures and one error, but their runner exits 0: inspect results rather than exit code alone. Both files compile. ruff unavailable. ING-003/004/007/009/010-I/N need fixes; installed/reader/maintenance behaviour is deferred. Design current-state text needs correction. Coordinator saved this result before remediation.

## TEST-BANK-001 r2 — repair checks

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| R1 | Inspect repairs and rerun four independent reproductions | Done | All four independent tests pass; actual results inspected |
| R2 | Run current suite and compile checks | Done | 37 unittest tests pass; both files compile |
| R3 | Confirm failure resolution, coverage and document state | Done | Four fixes confirmed; stale design text corrected; ruff not run |

Coordinator saved this checklist before independent retest. Earlier failed evidence remains above. No source edits authorised to Tester.

Final r2 result: Passed for four repairs and step 1 scope. Tester independently ran /tmp/test_bank_independent.py, unittest discovery and compilation with temporary pycache. All four repairs inspected. ING-010-A–N and tested money/account/card/balance/coverage/save-failure cases pass. No project edits. Reader, installed-skill and maintenance checks remain deferred; independent code/security reviews still required.

## TEST-BANK-001 r3 — complete review artifacts

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| H1 | Read specified actual files and record SHA256/line counts | Done | All 19 complete artifacts read and identified |
| H2 | Send complete numbered artifacts to code reviewer | Done | Complete contents plus administrative deltas delivered; no summaries substituted |
| H3 | Confirm coverage and return manifest | Done | Before hashes match original artifacts; actual final source hashes confirmed |

Reviewer lacks a permitted local reader but permits full comparison artifacts. Tester only supplies complete actual-file contents and verification, not delegated code review. No project edits or execution bypass. Record any missing/truncated artifact as a review blocker.

## TEST-BANK-001 r4 — code review repairs

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| V1 | Check full repair diff and before/after source/test hashes | Done | All 114 diff lines match fresh comparison of saved before files and actual files |
| V2 | Independently check three review defects, original four and full suite | Done | 41 suite tests, original four and separate three repair probes pass |
| V3 | Compile, check current document state and report limits | Done | Both files compile; current source hashes match; ruff unavailable |

Coordinator saved the specialist's proposed retest tasks before execution. Complete the outstanding H3 artifact manifest, then perform this independent retest. Source frozen at production hash 90a3fb3266cdb319b1269bb05047b78b29835ca7f884c1bf8aebbefe897254f1 and test hash d8c97c8224bce93f7ae5f00d7a218aa7bc937a435d16f50f3084fdfabb029677.

Final r3–r4 result: Passed. Tester verified full diff, before hashes, final files and all seven independent checks. Current production 732 lines; tests 480 lines. No project edits. Complete artifact set: both Python files; AGENTS; code-review, code-simplification and agent-planning skills; requirements; architecture; design; iterations; backlog; lifecycle; coordinator/developer/tester/designer/iteration-Product-Owner/code-reviewer/security-reviewer plans. Administrative changes were supplied as exact deltas after complete initial files. This is not a claim that later administrative edits retain old hashes. Final source/test hashes are those recorded immediately above and were checked after tests.

Commands: python3 /tmp/test_bank_independent.py; python3 /tmp/test_bank_reviewer_independent.py; python3 -m unittest discover -s tests/bank_statement_ingestion -v; compilation with PYTHONPYCACHEPREFIX=/tmp/bank-tester-pycache. Each result inspected. Reviewer supplied-content access remains a documented limit; installed skill/reader/maintenance checks deferred.

## TEST-BANK-001 r5 — remaining security artifacts

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| J1 | Read supplier manifest and identify undelivered records | Done | Eight remaining records identified after Developer's ten |
| J2 | Send complete current remaining records to Security Reviewer | Done | All eight full current records delivered, with hashes and line counts |
| J3 | Reconcile delivery, changed records and source hashes | Done | All 18 paths exist; 13 changed paths; no removed files; final source/test hashes unchanged |

Coordinator saved the specialist's initial plan before continuation. Developer supplies source/test/policies and approved inputs; Tester supplies remaining administrative records only. Source content need not be resent. The security verdict remains pending.

Final r5 checkpoint: all 18 complete artifacts supplied by Developer (10) and Tester (8); all 13 changed paths covered, no removal in supplied inventory. Tester confirmed current source/test hashes remain 90a3fb3266cdb319b1269bb05047b78b29835ca7f884c1bf8aebbefe897254f1 and d8c97c8224bce93f7ae5f00d7a218aa7bc937a435d16f50f3084fdfabb029677. Delivered tester plan was 63 lines/SHA256 75b86c568aa27973042c2bf331e997b553cfed4958b471e96b64a2b217d3509d; security plan 21 lines/SHA256 2a480994d3b9777e08931189864fb8152f67c6e70a497fabb42c37f6d9f89673. These identify reviewed versions before this administrative closure, not later file hashes. No tests or edits by Tester in r5. No original document comparison claimed. Final confirmation supplied directly to Security Reviewer.
