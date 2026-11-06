# Bank statement format revision 3 — Security repair re-check

Assignment SEC-BANK-FMT-003 r2. BL-001 scope revision 9, follow-up to APR-ING-IT4-002. Read-only review of `bank_history.py`, `statement_reader.py`, and `test_import_files.py`. Current hashes are in [the security repair plan](bank-statement-format-r3-security-repair-plan.md).

| Task ID | File / criterion | Planned action | Status | Result | Next action |
|---|---|---|---|---|---|
| SEC-R3-01 | `bank_history.py` | Check date-format type before membership and verify structured `FormatError` behavior | Done | Partly fixed: list-valued format returns `FormatError`, but malformed pair shapes or non-string field names can still raise raw `ValueError`/`TypeError. | Add shape validation and tests. |
| SEC-R3-02 | `statement_reader.py` | Check duplicate `workbookPr` entries fail closed | Done | Pass: duplicate workbook properties are rejected. | — |
| SEC-R3-03 | `test_import_files.py` | Check malformed-format/duplicate-epoch tests and zero record, transaction and coverage assertions | Done | Duplicate epoch test confirms no saved rows. Add malformed pair-shape and non-string field-name cases with no-save checks. | Add tests. |
| SEC-R3-04 | Three current hashes | Reconcile hashes with security repair plan and report closure | Done | Hashes match the security repair plan. Overall: SEC-FMT3-2 closed; SEC-FMT3-1 remains open for malformed pair structure. | Re-review after repair. |

## Initial checkpoint

The Reviewer inspected only the two prior security findings and their tests. SEC-FMT3-2 is closed. SEC-FMT3-1 remains open for malformed pair structure; the Developer is assigned a scoped repair and test.
