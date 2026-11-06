# Date and money format code review

Assignment REVIEW-ING-FMT r1. Read the approved [format checklist](bank-statement-format-iteration.md), `code-review`, `code-simplification`, and `security-privacy` skills. Review the actual current files against FMT-01–FMT-05. Do not edit source or tests.

| File | Current SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `3e550293bbbb12659f9f6e373a172d7e0cf409c42c5223b1ef4c437f72f9d1d7` |
| `skills/bank-statement-ingestion/SKILL.md` | `938035ee02a55747974b055f3c090313301b17bf3616410c5e83c21bc3305f63` |
| `tests/bank_statement_ingestion/test_import_files.py` | `e7262956353d20159d19dc5c4de2952f8dd50f0cd0bc7fea43876f14c49b468f` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `a601c5983a40d24316366ae434def7218e10875aa9bd7c8d44340000b85bad65` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `f01a87a657a848bf8698625b626b9a556e1113a4d1b9b77fe2eaf47c45fb4c9a` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1806b6a3c7c89ef62adb571dcec05a3d7901803c5dfc7499b6f59f590d3d1dec` |

The pre-edit SHA-256 values are in the main checklist. The original file copies are not available for byte-level comparison. Do not claim a full before/after review. Review the current implementation, requirements and tests; report this limit and any concrete findings with path and line.

## Review record

| Check | Status | Evidence / finding |
|---|---|---|
| Fixed format keys and strict conversion | Pass | Date and amount keys are fixed. Script conversion checks syntax, dates and precision. Unverified caller values are cleared. |
| Evidence and sign checks | Pass | Source text, cells, date-order evidence and sign evidence are checked and kept in source-linked fields. Conflicting signs and unclear date order remain unresolved. |
| Partial save and retry | Pass | Clear records save beside unresolved records. Format clarification keeps the source row identity. |
| Existing protections and history format | Pass | Reader source checks and atomic save flow remain. No database or reader change. |
| Simplicity | Pass with minor note | No needless layer or dependency. A duplicate `raw_date is None` check at `bank_history.py:1086` is unreachable; low priority. |
| Limit and verdict | Pass | All six reviewed hashes match. Original source copies are unavailable; no byte-level before/after claim. Full XLSX integration waits on `defusedxml==0.7.1`. |

## Repair review

The Coordinator acknowledged two review findings before repair: failed conversion could save unverified normalized values, and ambiguous slash dates lacked checked date-order evidence. Review the repaired files at the hashes above. Report whether both findings are closed; do not claim byte-level comparison because the original file copies are unavailable.

## Final review

Both findings are closed. The Code Reviewer passed the repaired changes and noted only the low-priority duplicate check above. The Security Reviewer passed all six files. The Code Reviewer verified all six hashes and the Tester independently verified the changed code/test hashes. Reviewers used current content and the saved baseline hashes; original file bytes were not available for a full comparison.

The date-role fixture now passes original posting-date text and its format key. Its current hash is `e7262956353d20159d19dc5c4de2952f8dd50f0cd0bc7fea43876f14c49b468f`. The affected test passed; no source code changed after review. The full suite passed in the prepared environment.

Final fixture recheck: the unique-location case selects the Amount cell and confirms that the script can match a single Posting date cell by its heading. The two-role case uses the same verified cell for both date fields and stays unresolved. Code review passed at test hash `a568d5eb45d41737674d5db44ca6bd1cfd2773f8397c192ff7084821f476f3d1`.
