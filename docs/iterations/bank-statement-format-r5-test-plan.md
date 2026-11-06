# Bank statement format test repair r5 — Developer checklist

Assignment: add missing tests for duplicate and unsupported date-format field names. Backlog item BL-001, test repair within the approved format-validation scope. Approved source scope: `tests/bank_statement_ingestion/test_import_files.py`. No production change is planned.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FMT-R5-001 | Review finding and baseline | Inspect the current malformed-format test and record baseline hash | Done | Existing cases test one-item pair and non-string field name. Duplicate date fields and unsupported string field names have no no-save cases. Baseline hash is below. | Wait for Coordinator acknowledgement before edits. |
| FMT-R5-002 | `test_import_files.py` | Add duplicate-field and unsupported-string-field cases; assert `FormatError`, zero statement records, transactions and verified coverage | Done | Added duplicate `transaction_date` and unsupported `statement_date` cases to the malformed-pair test. Each checks the field-level error and confirms no statement records, transactions or verified coverage. | Independent review. |
| FMT-R5-003 | Approved test path | Run focused and full bank statement tests, compilation and whitespace scan; report final hash | Done | Focused malformed-pair test passed. All bank statement tests passed (157 tests). `py_compile` passed. Whitespace scan is clean. Ruff is unavailable. No Git commands were run under role rules. | Coordinator should run Git checks. |

## Baseline hash

| Approved path | SHA-256 |
|---|---|
| `tests/bank_statement_ingestion/test_import_files.py` | `5d2f4b639340746f84e2cd5d29c75a33836405e1d9ee9d10e66d1922897a4ae7` |

## Next action

Send the test-only change and evidence to Coordinator for independent review. Git status and `git diff --check` remain unverified because this Developer role must not run Git commands.
