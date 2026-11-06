# BL-009 step 2 — Read safety fix checklist

Assignment DEV-TAG-IT2-RD r1. Backlog revision 8; BL-009 scope 2; approved step APR-TAG-IT2-001. This fixes findings from Tester, Code Reviewer and Security Reviewer revision 3. It does not change the approved design or add a table. Use generated test data only. Do not install dependencies or skills, use web search, or open real history.

## Baseline

| File | SHA-256 before edits |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `196700603502dbb31646aacc8a6a38dc63a5cb767b85f62063b3880d2d16c91b` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `03154fff6567a99efbfcf1325929d31381ffb713f9fa80d4e6813006146c1a4c` |
| `tests/bank_statement_ingestion/test_distribution.py` | `c7355f8a289edf7d3bb6e480c5026e54af353467beaeaf5f53c78092dd11cf3e` |
| `skills/bank-transaction-tagging/SKILL.md` | `19912a7d70e02aa8e88994570a01a0825912ca6258974362c584a41249687e61` |
| `README.md` | `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae` |
| `skills/CATALOG.md` | `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91` |

## Work checklist

| ID | File / requirement | Planned action | Status | Evidence / next action |
|---|---|---|---|---|
| RD-01 | `read_tagging_data` cursor | Reject non-string, empty, malformed and unknown IDs. Reject a cursor outside the selected account/date scope. Do not return an empty page that hides records. Keep UUID hex cursor format. | Done | Tests cover empty, malformed, non-string, unknown, cross-account and out-of-date cursors. |
| RD-02 | Tagging rules query | Restrict SQL to active rules for page account IDs and currencies. Limit to 201; if more than 200 relevant rules match, raise a clear `HistoryError`. Do not silently truncate. | Done | Test confirms 201 irrelevant rules do not affect selected scope and 201 relevant rules raise `HistoryError`. |
| RD-03 | Skill paging instructions | On every next-page read, repeat the same history, account/date filters and limit. Change only `after` to the prior `next_cursor`. | Done | Skill text and distribution assertions require the same filters and limit on each page. Filtered pagination test passes. |
| RD-04 | Regression checks | Run focused tests and compile; review diff against approved scope. | Done | `python3 -m pytest tests/bank_statement_ingestion/test_bank_history.py tests/bank_statement_ingestion/test_distribution.py -q`: 60 passed, 92 subtests passed. `python3 -m py_compile` passed for the helper and both test files. No dependency install or real history access. |

Developer confirmed this checklist and all six baseline hashes before edits. Coordinator acknowledges the checkpoint; implementation may proceed.

## Final file hashes

| File | SHA-256 after edits |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `817863c4487970b468cfde76610406747a98fd4c6776f01a9fdc8f3a03b90c1c` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `450c92b2a6db9bc41429f44cc2f88f99952d5753b53076fd697d0040848e1f28` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1d0bf07a8ab4f3a265829579f2bdb581825f36ce64c3e37b62a8f4f6c054fbad` |
| `skills/bank-transaction-tagging/SKILL.md` | `41a21a2f4f14b6da6fd0655de86eb359ea289168fe3b22d4272c26354854cdce` |
| `README.md` | `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae` |
| `skills/CATALOG.md` | `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91` |

## Limits

- The result keeps the existing transaction page default of 50 and maximum of 200.
- Rule results above 200 stop with an error. They are not truncated.
- No schema, storage, privacy, encryption or product behavior change beyond the three review fixes.
