# BL-009 step 2 — Code Reviewer checklist, revision 3

Assignment REVIEW-TAG-IT2 r3. Backlog revision 8; BL-009 scope 2; step approval APR-TAG-IT2-001. Prior revisions remain preserved. Review the stable bounded-read change and its integration with the existing privacy and tagging fixes. Do not edit files or run tests.

| Task ID | File / check | Planned review | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| R3-01 | `bank_history.py` | Check limit validation, stable keyset cursor, query scope, returned fields and cursor only when more rows exist | Done | Fail. Cursor and transaction paging are stable, but invalid cursors are not checked against transaction ID format or selected scope. Rules are still unbounded and are filtered after loading. | Fix both issues |
| R3-02 | `test_bank_history.py` | Check multi-page coverage and boundary tests | Done | Fail. Tests cover valid traversal but not malformed/out-of-scope cursors or rule result limits. | Add tests |
| R3-03 | Tagging `SKILL.md` | Check one-page-at-a-time instruction | Done | Fail. The next-page call does not say to repeat the same account/date filters and page size; this can widen the selected scope. | Preserve filters explicitly |
| R3-04 | `test_distribution.py` | Check bounded-read contract assertion | Done | Pass for bounded transaction page only. Does not assert filter retention or bounded rules. | Extend assertions |
| R3-05 | Cross-file behavior | Check cursor use does not expose dates or break account/currency filtering | Done | Fail. Follow-on reads can drop account/date scope; query itself applies supplied filters before cursor. | Fix skill and add filtered-page test |
| R3-06 | Hashes and evidence | Compare current six-file inventory to Developer plan | Done | Pass. Hashes matched the bounded-read Developer plan. Reviewer did not run tests. | New review after fixes |

No code change or test run by Reviewer. No real data.

Verdict: Fail pending fixes. Reviewer found that every follow-on page must repeat the original account/date filters, and noted that tagging rules remain unbounded. No tests or file changes were made by Reviewer.
