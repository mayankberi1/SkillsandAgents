# Bank statement format repair r4 — Developer checklist

Assignment: validate `Record.date_formats` structure before any unpacking or dictionary construction. Backlog item BL-001, implementation repair. Approved paths: `bank_history.py` and `test_import_files.py`. Preserve the r2 and r3 fixes.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FMT-R4-001 | Review finding and baseline | Inspect date-format uses and record baseline hashes | Done | `_convert_record` builds a dict before validating pair shape. `_verify_source` also unpacks each pair before conversion. Baseline hashes are below. | Wait for Coordinator acknowledgement before source edits. |
| FMT-R4-002 | `bank_history.py` | Validate outer collection, pair length, supported string field name, string format and duplicate field before unpacking or dict creation; return structured field error | Done | Added structural validation before `_convert_record` builds dictionaries and before `_verify_source` unpacks date-format entries. Malformed values return a date-format `FormatError`. | Independent review. |
| FMT-R4-003 | `test_import_files.py` | Add one-item pair and non-string field tests; assert `FormatError` and no transactions, statement records or verified coverage | Done | Added both required regression cases. Both check field-level errors and zero statement records, transactions and verified coverage. The earlier unhashable format test also passes. | Independent review. |
| FMT-R4-004 | Two approved paths | Run focused and full tests, compilation and whitespace scan; report final hashes | Done | Two focused malformed-format tests passed. All tests in the bank statement folder passed (157 tests). `py_compile` passed. Whitespace scan is clean. Ruff is unavailable. No Git commands were run under role rules. Final hashes are below. | Coordinator should run Git checks. |

## Baseline hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `6ff4a00dabd9036f093948210eb10e41dc5ffa63dd1e1eae1ef03c303edcfea3` |
| `tests/bank_statement_ingestion/test_import_files.py` | `71a04b4f6dd15cffb5637559ba0883101b68f4e8e60fa40d3e16d6fc8cffc1ba` |

## Final hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `8abd02e6561141cb3f6e60b0ac08baba74f438bcd5efb7a42f66a561f32c2a6e` |
| `tests/bank_statement_ingestion/test_import_files.py` | `a2f2d11acf2a954e0ab11abf2de61ea4ea384760d1b4489ed77ff766224388bb` |

## Next action

Send the scoped change and evidence to Coordinator for independent review. Git status and `git diff --check` remain unverified because this Developer role must not run Git commands.
