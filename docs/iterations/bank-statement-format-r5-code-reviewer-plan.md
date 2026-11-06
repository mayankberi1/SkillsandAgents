# Bank statement format repair R4 — Code review checklist

Assignment REVIEW-BANK-FMT-004 r1. BL-001 scope revision 9, focused review of approved APR-ING-IT4-002 repairs. Read-only review. Current hashes are in the R4 Developer plan and R3 security repair plan.

| Task ID | File / criterion | Planned action | Status | Result | Next action |
|---|---|---|---|---|---|
| FMT-R5-001 | Inputs and baselines | Compare current hashes with R4 and R3 final hashes; record requirements and limits | Done | `bank_history.py` and `test_import_files.py` match R4 final hashes; `statement_reader.py` matches R3 final hash. | — |
| FMT-R5-002 | `bank_history.py` | Verify malformed `Record.date_formats` collection/pair shape, field name, format type and duplicates produce structured `FormatError` before writes | Done | `_date_format_structure_error` checks collection, pair size, field type/name, format type, and duplicates before dictionary construction. `_verify_source` calls it before the later loop unpacks formats. `_verify_source` raises accumulated errors before `_save_statement` opens its write connection. Duplicate and unsupported string field behavior were checked by code only; tests do not cover these two cases. | Add regression cases if the Coordinator requires full test coverage for each branch. |
| FMT-R5-003 | `statement_reader.py` | Verify duplicate `workbookPr` is rejected without choosing an epoch | Done | `_xlsx` rejects more than one direct `workbookPr` before it sets the workbook epoch. | — |
| FMT-R5-004 | `test_import_files.py` | Verify no-save assertions for statement records, transactions and verified coverage; confirm amount evidence P2 parser fix remains | Done | Malformed format cases and duplicate workbook epoch case assert zero `statement_records`, zero transactions, and zero `periods` with kind `verified`. The amount evidence parser still splits only on `'; '`, validates each named value, rejects whitespace in empty values, and matches supplied values. The reviewed amount code hash matches R4 baseline, which matches R3 final. | — |
| FMT-R5-005 | Verdict and evidence | Inspect scope and code quality; report findings, limits and final hashes | Done | No code defect found. The initial low-severity test gap was closed in review r2: duplicate date field and unsupported string field no-save cases were added and independently verified. The Reviewer did not run tests. | — |

## Current hashes

| Reviewed path | SHA-256 | Expected plan hash |
|---|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `8abd02e6561141cb3f6e60b0ac08baba74f438bcd5efb7a42f66a561f32c2a6e` | R4 final |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `048b9a58af98f5de261647a5cbad0da87cd21ea8ed83992fa57dff4b99afe966` | R3 final |
| `tests/bank_statement_ingestion/test_import_files.py` | `a2f2d11acf2a954e0ab11abf2de61ea4ea384760d1b4489ed77ff766224388bb` | R4 final |

## Initial checkpoint

The Reviewer read the saved R4 Developer plan and R3 security review. The repository's agent-planning file is missing in the shared workspace; the Coordinator read and applied it earlier in the task. The Reviewer has not inspected code. The Coordinator must acknowledge this checklist before review starts.
