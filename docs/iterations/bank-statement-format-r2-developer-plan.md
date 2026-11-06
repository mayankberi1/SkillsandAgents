# Bank statement format repair r2 — Developer checklist

Assignment: separator-evidence parser repair, r2. Backlog item BL-001; implementation repair after independent review. Approved scope for this repair: `bank_history.py` and `test_import_files.py`; preserve all prior approved behavior. The P2 finding is that optional whitespace in the regular expression can treat `group_separator= ;` as an empty group separator.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FMT-R2-001 | Approved finding and baseline | Read the current evidence parser and amount tests; record exact hashes and scope | Done | `_amount_evidence_problem` uses `\s*` around values. `group_separator= ;` can match an expected empty value. Baseline hashes are below. | Wait for Coordinator acknowledgement before source edits. |
| FMT-R2-002 | `bank_history.py` | Parse the three named evidence values exactly, without trimming a separator value; retain supported marks and existing validation | Done | Split only at the documented `; ` field boundary, parse each exact field name once, and compare the full value. A literal space stays part of the group separator value. | Independent review. |
| FMT-R2-003 | `tests/bank_statement_ingestion/test_import_files.py` | Add a regression case where whitespace falsely claims an empty group mark; confirm the import stops and saves no transaction or coverage | Done | Added `space-must-not-mean-empty` to the import tests. It rejects `group_separator= ;` when the selected separator is empty and confirms no financial rows or coverage save. | Independent review. |
| FMT-R2-004 | Two approved source paths | Run focused and full bank statement tests, compilation and whitespace scan; report final hashes | Done | Focused regression: 1 passed. All five bank statement test files: 154 passed. `py_compile` passed. Whitespace scan is clean. Ruff is unavailable. No Git command was run under role rules. Final hashes are below. | Coordinator should run Git checks. |

## Baseline

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `1ecc8b5f9cb901c7be96a8d0e2bc800fdf28bc631ac61ff4531aa81935d6b44a` |
| `tests/bank_statement_ingestion/test_import_files.py` | `9aabf02c8e1900d1d84689009dd8bc80d10be0e8ad4768f6b8715469c5f621ee` |

## Final hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `b83f9b8f2efba2c60c577a159a1599c19d8e5840cbb1d5176c9d5c7a369f452c` |
| `tests/bank_statement_ingestion/test_import_files.py` | `b180e4b0fdd297a7d04cd709699025c98fca00ae7cb0db270344ecada9a05df6` |

## Next action

Send the repair and its evidence to Coordinator for independent review. Git status and `git diff --check` remain unverified because this Developer role must not run Git commands.
