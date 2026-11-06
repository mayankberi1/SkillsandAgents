# Bank statement format security repair r3 — Developer checklist

Assignment: repair malformed date-format handling and duplicate XLSX epoch metadata. Backlog item BL-001, implementation repair. Approved source/test scope: `bank_history.py`, `statement_reader.py`, and `test_import_files.py`. Preserve prior approved behavior and the r2 amount-evidence fix.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FMT-R3-001 | Review finding and three-path baseline | Inspect date format dispatch, workbook property parsing and existing no-save tests; record hashes | Done | Date format membership checks set membership before confirming a string. Reader selects the first `workbookPr`. Amount and epoch failure tests do not all assert zero statement records. Baseline hashes are below. | Wait for Coordinator acknowledgement before source edits. |
| FMT-R3-002 | `bank_history.py` | Guard date format membership by string type so malformed values become field-level `FormatError` | Done | The Excel serial membership check now runs only for strings. A malformed list format reaches date conversion and returns its existing field-level `FormatError`. | Independent review. |
| FMT-R3-003 | `statement_reader.py` | Reject duplicate workbook epoch properties rather than choosing one | Done | Reader counts workbook properties and rejects more than one with a clear unsupported-read result. | Independent review. |
| FMT-R3-004 | `tests/bank_statement_ingestion/test_import_files.py` | Add malformed unhashable date-format and duplicate epoch no-save tests; assert zero `statement_records` in amount and epoch failure cases | Done | Added a malformed-list date test and a conflicting duplicate-epoch XLSX test. Both assert zero statement records, transactions and verified coverage. Amount-evidence and epoch-failure cases now also assert zero statement records. | Independent review. |
| FMT-R3-005 | Three approved paths | Run focused/full tests, compilation and whitespace scan; report final hashes and limits | Done | Four focused cases passed; all tests in the bank statement folder passed (156 tests); `py_compile` passed; trailing-whitespace scan is clean. Ruff is unavailable. No Git commands were run under role rules. | Coordinator should run Git checks. |

## Baseline hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `b83f9b8f2efba2c60c577a159a1599c19d8e5840cbb1d5176c9d5c7a369f452c` |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `e0c05dc1e5738a98832bcd3d7ea63e66fd9cf6a7fe07ad622508eca83750aaf3` |
| `tests/bank_statement_ingestion/test_import_files.py` | `b180e4b0fdd297a7d04cd709699025c98fca00ae7cb0db270344ecada9a05df6` |

## Final hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `6ff4a00dabd9036f093948210eb10e41dc5ffa63dd1e1eae1ef03c303edcfea3` |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `048b9a58af98f5de261647a5cbad0da87cd21ea8ed83992fa57dff4b99afe966` |
| `tests/bank_statement_ingestion/test_import_files.py` | `71a04b4f6dd15cffb5637559ba0883101b68f4e8e60fa40d3e16d6fc8cffc1ba` |

## Next action

Send the source and test changes to Coordinator for independent review. Git status and `git diff --check` remain unverified because this Developer role must not run Git commands.
