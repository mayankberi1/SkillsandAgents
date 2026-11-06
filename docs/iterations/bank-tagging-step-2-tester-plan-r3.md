# BL-009 step 2 — Tester checklist, revision 3

Assignment TEST-TAG-IT2 r3. Backlog revision 8; BL-009 scope 2; step approval APR-TAG-IT2-001. Revisions 1–2 remain preserved. Use generated data only; do not install dependencies or skills, use web search, or open real history.

| Task ID | File / criterion | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| T2X-01 | `read_tagging_data` | Check default/max page limits, invalid limits and single-transaction behavior | Done | Fail. Page sizes are checked, but `after='not-a-valid-id'`, `after=''` and `after=123` are accepted; the invalid string can return an empty final page and omit rows. | Reject malformed/unknown/out-of-scope cursors and add tests |
| T2X-02 | `read_tagging_data` | Walk more than one page; check stable order, no duplicates/omissions, correct end cursor | Done | Fail. Valid cursor traversal passed for 203 generated rows, but an invalid cursor can silently skip all rows. | Repeat after cursor fix |
| T2X-03 | `test_bank_history.py`, `test_distribution.py` | Run focused tests and compile | Done | Pass before cursor correction. Focused run: 57 tests, 85 subtests. Compile passed. | Re-run after fix |
| T2X-04 | Full ingestion tests | Run the relevant full suite and record missing-dependency limits | Done | Limited. 128 passed, 12 failed, 116 subtests. Failures require missing `defusedxml==0.7.1`; no dependency installed. | Do not install `defusedxml` |

No source edits by Tester.

Code Reviewer r3 also found that the skill does not repeat account/date filters on later pages, so a later page can include rows outside the initial scope. Security Reviewer r3 found all matching tagging rules are returned without a count limit, and the helper reads irrelevant rules before filtering. Step 2 remains open until these issues are fixed and retested.
