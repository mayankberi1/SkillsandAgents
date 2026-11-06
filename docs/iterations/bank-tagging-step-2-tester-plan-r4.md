# BL-009 step 2 — Tester checklist, revision 4

Assignment TEST-TAG-IT2 r4. Backlog revision 8; BL-009 scope 2; step approval APR-TAG-IT2-001. Prior review records remain preserved. Use generated histories only; do not install packages or skills, use web search, or open real history.

| File | SHA-256 before tests |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `196700603502dbb31646aacc8a6a38dc63a5cb767b85f62063b3880d2d16c91b` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `03154fff6567a99efbfcf1325929d31381ffb713f9fa80d4e6813006146c1a4c` |
| `tests/bank_statement_ingestion/test_distribution.py` | `c7355f8a289edf7d3bb6e480c5026e54af353467beaeaf5f53c78092dd11cf3e` |
| `skills/bank-transaction-tagging/SKILL.md` | `19912a7d70e02aa8e88994570a01a0825912ca6258974362c584a41249687e61` |
| `README.md` | `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae` |
| `skills/CATALOG.md` | `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91` |

| Task ID | File / criterion | Planned action | Status | Result / next action |
|---|---|---|---|---|
| T2Y-01 | Six-file baseline | Record and reconcile hashes | Done | Exact six-file baseline above. |
| T2Y-02 | `read_tagging_data` cursor | Test malformed, non-string, empty, unknown and out-of-scope cursors | Pending | Use generated accounts and transactions. |
| T2Y-03 | Filtered paging | Walk pages with account and date filters; verify every next-page call preserves scope, order, and complete coverage | Pending | Use generated histories only. |
| T2Y-04 | Rule query and result cap | Verify account/currency scope; test 200 and 201 matches; require a clear error above 200 and no silent truncation | Pending | Use generated rules only. |
| T2Y-05 | Focused tests and compile | Run changed history/distribution tests and compile affected Python files | Pending | No installs. |
| T2Y-06 | Broader suite | Run full ingestion tests and record environment limits | Pending | Earlier run had 12 XLSX failures because `defusedxml==0.7.1` is absent. Do not install it. |

No independent tests have started. The original pre-edit baseline is preserved above.

## Coordinator acknowledgement and result

The Developer completed the scoped fix. Final hashes are recorded in [Developer checklist](bank-tagging-step-2-read-fix-plan.md). Coordinator confirms the changed files match the approved scope and acknowledges this test plan. The Tester may now run independent checks.

## Independent test results

| Task ID | Status | Result |
|---|---|---|
| T2Y-01 | Done | Final six-file hashes match the Developer checklist and current files. |
| T2Y-02 | Pass | Generated tests reject empty, malformed, non-string, boolean, unknown, cross-account and out-of-date cursors. Single-transaction lookup with a cursor also fails. |
| T2Y-03 | Pass | 203 rows traversed in stable order across 37-row pages with no duplicates or omissions. Account/date-filtered pages return only the selected set; skill says to repeat the filters and limit. |
| T2Y-04 | Pass | SQL scopes rule reads to page account IDs and currencies. Checked-in tests cover irrelevant rules and the 201-rule error. Separate generated check confirms 200 matching rules return all 200 and 201 raises `HistoryError`. |
| T2Y-05 | Pass | Focused pytest: 60 passed, 92 subtests. `compileall` passed. Python 3.14.4; pytest 9.0.2. |
| T2Y-06 | Limited | Full ingestion suite: 131 passed, 12 failed, 123 subtests. All failures need missing `defusedxml==0.7.1` for XLSX tests. No package was installed. |

Verdict: Pass for the approved step 2 scope. The full suite remains limited by the missing dependency. No source edits, installs, web requests or real-history use by Tester. No full-repository suite was run.
