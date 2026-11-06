# BL-009 step 1 — Tester checklist

Assignment TEST-TAG-IT1 r1. Backlog revision 8; BL-009 scope 2; queue revision 8. Requirements APR-ING-REQ-006, architecture APR-ING-ARCH-003, design APR-ING-DES-005, step approval APR-TAG-IT1-001. Stage: independent testing. No real history or dependency installation.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| T1-01 | `bank_history.py`; TAG-001, 002, 007, 008 | Check format-2 fields, rules, approval gate and named-column writes; verify IDs and financial fields stay unchanged | Done | Pass. Fields/rules are present; update checks approval; new inserts name columns; IDs and financial values are preserved in generated test history. | — |
| T1-02 | Same source; update rules | Use generated data to check refusal, successful update and rollback after injected failures | Done | Pass. Refusal and injected failures leave the generated database at format 1; successful update sets format 2 and preserves transaction values. | — |
| T1-03 | `test_bank_history.py`; TAG-001/002/007/008/009 | Check tests and run focused cases for fields, rules, approval, update, failures and preservation | Done | Pass. Focused tests passed. | — |
| T1-04 | `test_maintenance.py`; TAG-008/010 | Check export/restore, account deletion choices, stale-choice rejection, and full deletion | Done | Pass. Focused tests passed for export/restore and deletion cases. | — |
| T1-05 | `test_distribution.py`, ingestion `SKILL.md`; TAG-007/008 | Check installed-copy expectations and user approval instructions | Done | Pass. Installed copy expects helper 1/database format 2; skill asks before updating a saved history. | — |
| T1-06 | `docs/iterations/bank-ingestion-solution.md` | Reconcile BL-001 storage notes with approved BL-009 design revision 4 | Done | Pass. Storage notes match format 2 and one-transaction update. | — |
| T1-07 | Test environment and changed-file inventory | Run focused checks and compilation; review known dependency failures without installing packages | Done | Python 3.14.4, pytest 9.0.2. Focused run: 97 passed, 70 subtests passed. `compileall` passed. Wider ingestion suite: 118 passed, 12 failed because `defusedxml==0.7.1` is missing. Ruff is unavailable. Full repository collection was not run by Tester; Developer reports missing Google libraries. | Do not install packages; no real history used |

Final inventory: six changed implementation files, including `test_distribution.py`, which had a format-1-only assertion. Independent test verdict: Pass for the approved step-1 behavior. The 12 wider-suite failures are dependency-related; the missing dependency was not installed. TAG-003/004/005/006/009 tagging behaviors are step 2 and were not tested here. No source edits, real data, or dependency installation occurred.
