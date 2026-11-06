# BL-009 step 2 — Developer fix checklist

Assignment DEV-TAG-IT2-FIX r1. BL-009 scope revision 2; step approval APR-TAG-IT2-001. This assignment fixes findings from the independent Code Reviewer and Tester. It does not add a new feature or change the approved scope. Do not install skills, use web search, or open/update a real history. Coordinator saved and acknowledged this checklist before source edits.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FIX-01 | `bank_history.py`; TAG-005 | Preserve source URL/title/date/uncertainty when a partial user update leaves the cited vendor unchanged; do not retain source for a replaced vendor | Done | Regression tests pass for source retention and stale-source clearing. | Review updated file |
| FIX-02 | `bank_history.py`; TAG-002 | Keep one-time user-selected tags ahead of later matching rules, including when user tags are the only selected field | Done | Regression test confirms tags-only user choice survives rule application. | Review updated file |
| FIX-03 | `bank_history.py`; rule results | Set vendor/category status to `rule_confirmed` when a rule supplies those values | Done | Regression tests confirm rule-supplied statuses. | Review updated file |
| FIX-04 | New tagging `SKILL.md`; TAG-006 | State that unanswered questions leave transactions unchanged and unresolved | Done | Skill now states the no-answer behavior. | Review wording |
| FIX-05 | Tests | Add regression tests for each finding; use generated histories | Done | Added source-preservation, stale-source, tags-only priority and rule-status tests; generated histories only. | — |
| FIX-06 | Verification and handoff | Run focused tests, compile checks and available checks; report new hashes and changed files | Done | Focused tests: 54 passed, 63 subtests passed. Compile passed. No real history or dependency used. | Independent reviews required |

Independent findings are saved in [the Code Reviewer plan](bank-tagging-step-2-code-reviewer-plan.md) and [the Tester plan](bank-tagging-step-2-tester-plan.md). Baseline and scope were checked before edits. Fixes are limited to the three listed files. Final SHA-256 values: `bank_history.py` 6916d747cae036675c218bb7738151bd1164480998b0e8f2a08bc0ee2eafd77f; `test_bank_history.py` 37c673e2259444253e588446a478738181fd5a81276b26edf276031fd439ba70; tagging `SKILL.md` 835311caebe70d75c6e3799b500b7b0f05517d27362b17f284822d90eb72dd49. Security review findings remain open.
