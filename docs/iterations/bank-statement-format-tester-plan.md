# Date and money format test review

Assignment TEST-ING-FMT r1. Read the approved [format checklist](bank-statement-format-iteration.md) and `testing-verification` skill. Independently check the current tests and run useful cases. Do not edit source or tests.

| File | Current SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `3e550293bbbb12659f9f6e373a172d7e0cf409c42c5223b1ef4c437f72f9d1d7` |
| `tests/bank_statement_ingestion/test_import_files.py` | `e7262956353d20159d19dc5c4de2952f8dd50f0cd0bc7fea43876f14c49b468f` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `a601c5983a40d24316366ae434def7218e10875aa9bd7c8d44340000b85bad65` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `f01a87a657a848bf8698625b626b9a556e1113a4d1b9b77fe2eaf47c45fb4c9a` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1806b6a3c7c89ef62adb571dcec05a3d7901803c5dfc7499b6f59f590d3d1dec` |

The pre-edit SHA-256 values are in the main checklist. Test files are ignored by Git in this repository; check the files in the shared workspace and state this limit. Do not use real statements or install packages.

## Review record

| Check | Status | Evidence / finding |
|---|---|---|
| Supported date and amount keys | Pass | Focused tests cover listed text formats and all amount keys. Excel serial conversion helper passes; reader integration is blocked by missing dependency. |
| Unclear and invalid values | Pass | Checked ambiguous order with matching/conflicting evidence, invalid values, unsupported keys and excess precision. |
| Sign evidence and source details | Pass | Checks signs, source evidence, raw values, keys and locations. |
| Partial import and retry | Pass | Clear rows save; unclear rows remain unresolved; clarification retries the same record. |
| Run record | Pass | Independent focused run: 6 passed, 13 subtests. Final four-file run: 142 passed, 125 subtests in the existing prepared environment. No installs or real data. |

## Repair recheck

The repaired tests cover date-order evidence and clearing unconverted normalized values. The independent recheck passed focused date/evidence/invalid-value tests: 6 passed, 13 subtests.

The final four-file run passed 142 tests and 125 subtests. It used the existing `/tmp/bank-step2-reader-env` with `defusedxml==0.7.1`; no package was installed. An older test fixture first failed because it omitted the new posting-date raw text and key. The Developer fixed the fixture, and the test then passed. XLSX reader integration passed.

Final fixture recheck: `test_import_files.py` hash is `a568d5eb45d41737674d5db44ca6bd1cfd2773f8397c192ff7084821f476f3d1`. The unique Posting date cell case supplies the missing location from its header and saves the row; the same-cell/two-role case stays unresolved. Both focused tests passed. The full four-file suite passed: 142 tests and 125 subtests.
