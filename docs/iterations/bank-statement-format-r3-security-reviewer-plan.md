# Bank statement format revision 3 — Security review checklist

Assignment SEC-BANK-FMT-003 r1. BL-001 scope revision 9, implementation security review. Approval APR-ING-IT4-002. Read-only review of the eight approved paths. Final hashes are in [the Developer plan](bank-statement-format-r3-developer-plan.md) and P2 repair plan.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| SEC-001 | `.gitignore` | Check the added test visibility exception is narrow and does not expose unrelated ignored files | Done | Pass. Approved tests are visible; other tests remain ignored. | — |
| SEC-002 | `bank_history.py` | Review format strings, evidence binding, user-answer handling, epoch checks, save/audit behavior and prior repairs | Done | Fail, Low SEC-FMT3-1: date format membership check occurs before string/type validation; malformed values can escape as raw `TypeError`, not `FormatError`. | Add early shape/type check and no-save test. |
| SEC-003 | `statement_reader.py` | Review reader limits and workbook epoch extraction passed to history checks | Done | Fail, Medium SEC-FMT3-2: duplicate `workbookPr` elements are not rejected; conflicting date epochs can be silently resolved by taking the first. | Reject duplicates and test no-save. |
| SEC-004 | `SKILL.md` | Check privacy, untrusted statement content, format inputs and confirmation instructions | Done | Pass. Clear format, evidence, no-guess and retry instructions. | — |
| SEC-005 | `test_bank_history.py` | Check security validation, ambiguity, exact amounts, errors and no-save cases | Done | Pass; unchanged approved hash. | — |
| SEC-006 | `test_import_files.py` | Check source/header/cell evidence, user answers, epoch mismatch and full-statement abort | Done | Pass with test gap: amount and epoch failures do not explicitly assert zero statement-record rows; source path confirms pre-write failure. | Add assertion with fixes. |
| SEC-007 | `test_maintenance.py` | Check for unintended exposure or unsafe maintenance behavior | Done | Pass; synthetic data only. | — |
| SEC-008 | `test_distribution.py` | Check distribution assertions and ignore scope | Done | Pass. | — |
| SEC-009 | Inventory and baseline | Reconcile all eight paths, hashes, approved scope and prior finding repairs | Done | All eight hashes match Developer and P2 repair records; prior separator, date-length, overlap, date-location and evidence-parser findings were rechecked. | Reconcile after fixes. |
| SEC-010 | Whole-statement stop and privacy | Verify invalid formats/epochs save no financial or coverage data; inspect audit content | Done | Format errors stop before source/statement/record/transaction/coverage writes. Existing failure audit stores filename and short reason only. Prior history remains. | Explicitly assert record count in amount/epoch tests. |
| SEC-011 | Reader security limits | Verify source checks, bounds, formula/external-link handling and locations | Done | Limits and checks remain. No real data, network or install. Duplicate epoch metadata issue recorded under SEC-FMT3-2. | Fix and re-review. |
| SEC-012 | Final report | Record per-file verdicts, findings, limits and next action | Done | Overall Needs Changes: `bank_history.py` Fail (Low); `statement_reader.py` Fail (Medium); all other paths Pass, with listed test gap. No tests or scanner run by reviewer. | Re-review after fixes. |

## Initial checkpoint

The Reviewer read `agent-planning` and `security-privacy` instructions. The Coordinator acknowledged this checklist before review. The findings and limits above are the initial security result. The Developer must fix both findings and add explicit no-save record-count assertions before re-review.
