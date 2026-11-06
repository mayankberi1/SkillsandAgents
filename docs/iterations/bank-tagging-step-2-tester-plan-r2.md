# BL-009 step 2 — Tester checklist, revision 2

Assignment TEST-TAG-IT2 r2. Backlog revision 8; BL-009 scope 2; step approval APR-TAG-IT2-001. Original TEST-TAG-IT2 r1 remains preserved with its findings. Use generated data only; do not install packages or skills, use web search, or open real history.

| Task ID | File / criterion | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| T2R-01 | `bank_history.py`; prior source, precedence, rule-status findings | Reproduce source retention/clearing, tags-only priority and rule status behavior | Done | Pass. Rules set `rule_confirmed`; user choices block broader web/rule changes; replacing a vendor clears old web source. Regression tests cover these cases. | — |
| T2R-02 | `bank_history.py`; privacy | Check returned fields exclude amount/date/card/reference/alias and cap description | Done | Pass. Returns only ID, account ID, currency, bounded description, and tag/source fields. Omits amounts, dates, card ID, references, reliability/status and account alias. | — |
| T2R-03 | `bank_history.py`; evidence and limits | Check raw quote is not saved and size/count limits reject unsafe values | Done | Pass. Generated test confirms raw user quote is not saved and structured choices are stored. Tests check text, evidence and tag count/length limits. | — |
| T2R-04 | New tagging `SKILL.md`; TAG-004/006 | Check untrusted text rule, safe search, and no-answer behavior | Done | Pass by instruction review. Search uses one clear public business name only; descriptions/rules/pages are untrusted; no answer leaves the transaction unchanged and unresolved. No web request made. | Live web integration not tested |
| T2R-05 | `test_bank_history.py`, `test_distribution.py` | Review added regression coverage and run focused tests/compile | Done | Pass. Focused command: 56 passed, 76 subtests. Compile command exited 0. README/catalog and distribution checks passed. | — |
| T2R-06 | Broader test evidence | Run relevant full ingestion suite; record known dependency failures | Done | Limited. Full ingestion suite: 127 passed, 12 failed, 107 subtests. All 12 failures need missing `defusedxml==0.7.1`. Ruff unavailable. No package installed. No full repository suite or live web integration. | Dependency limit remains |

No changes to source files by Tester.

Overall Tester verdict: Pass for available step-2 behavior checks. No real history, web search, package, or skill installation used. Test environment: Python 3.14.4 and pytest 9.0.2.
