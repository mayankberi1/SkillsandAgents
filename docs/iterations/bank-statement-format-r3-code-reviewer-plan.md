# Bank statement format revision 3 — Code review checklist

Assignment REVIEW-BANK-FMT-003 r1. Backlog BL-001, scope revision 9. Approvals APR-ING-DES-007 and APR-ING-IT4-002. Read-only review of the eight approved paths; final hashes are in [the Developer plan](bank-statement-format-r3-developer-plan.md).

| Task ID | Path / criterion | Planned action | Status | Result | Next action |
|---|---|---|---|---|---|
| CRF3-01 | `.gitignore` | Verify ignore exception tracks only approved bank tests | Done | Pass. Approved tests appear as `?? tests/`; unrelated `tests/other/example.py` remains ignored. | — |
| CRF3-02 | `bank_history.py` | Review amount evidence relevance, source checks, user answers, ambiguity decision, canonical dates, epoch enforcement, date location, whole-file no-save | Done | **Fail (P2):** evidence parser regex at current line 854 treats whitespace after `=` as optional syntax and can misread `group_separator= ;` as an empty group mark. Exact parser and regression test needed. | Repair and re-review. |
| CRF3-03 | `statement_reader.py` | Verify reader epoch source, metadata, and safety limits | Done | Pass. Epoch comes from protected workbook metadata and appears as `1900` or `1904`; existing read limits remain. | — |
| CRF3-04 | ingestion `SKILL.md` | Check exact caller instructions, evidence use, failure/retry guidance | Done | Pass. Instructions match design 6. | — |
| CRF3-05 | `test_bank_history.py` | Verify acceptance coverage, especially overlap and date location fixtures | Done | Pass. Overlap fixture reaches the intended conflict path; date error test checks row fallback. | — |
| CRF3-06 | `test_import_files.py` | Verify reader epoch, styled/un-styled date, amount evidence and whole-file failure tests | Done | Pass with gap: add regression for whitespace group evidence conflicting with empty group separator. | Repair and re-review. |
| CRF3-07 | `test_maintenance.py` | Check preservation of maintenance behavior | Done | Pass; unchanged. | — |
| CRF3-08 | `test_distribution.py` | Verify distributed content checks | Done | Pass. | — |
| CRF3-09 | Cross-file scope / hashes / simplification | Check all eight approved paths, current hashes against Developer's final hashes, scope, preserve earlier findings/failures | Done | All eight hashes match. Scope matches approval. No schema/dependency changes or unnecessary layers. | Reconcile after repair. |
| CRF3-10 | Verification evidence | Assess Developer's test evidence and any needed independent checks | Done | Reviewer did not run tests. Developer reports 154 tests and compilation pass, Ruff unavailable. Reviewer verified ignore behavior; original baseline byte comparison unavailable. | Re-run tests after repair. |

## Initial checkpoint

The Reviewer read code-review and agent-planning instructions, the Developer plan and the approved scope. Earlier date-location and overlap-fixture findings were repaired. Amount-evidence and Excel-epoch findings have approval APR-ING-DES-007 and implementation approval APR-ING-IT4-002. No substantive review has started. The Coordinator must acknowledge this checklist first.
