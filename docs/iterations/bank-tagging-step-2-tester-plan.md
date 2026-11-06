# BL-009 step 2 — Tester checklist

Assignment TEST-TAG-IT2 r1. Backlog revision 8; BL-009 scope 2; queue revision 8. Requirements APR-ING-REQ-006, design APR-ING-DES-005 and step approval APR-TAG-IT2-001. Use generated data only. Do not install dependencies or skills, use web search, or open real history.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| T2-01 | `bank_history.py`; TAG-001–010 | Check read/save functions, rule priority, account/currency scope and unchanged financial/link fields | Done | Fail. Rule application leaves vendor/category statuses as `unknown` instead of `rule_confirmed`; reproduced with generated data at lines 1099–1116. Shared and account rule scopes and preservation of user-confirmed vendor/category pass. | Fix rule status and repeat affected checks |
| T2-02 | `test_bank_history.py` | Review and run generated-data tests for user confirmation, web suggestions, rules, invalid values, save failures and preservation | Done | Fail. Existing rule test does not assert rule-confirmed statuses. Focused tests passed, but the missing assertion allowed the defect. | Add status regression test and rerun |
| T2-03 | New tagging `SKILL.md` | Check user flow, safe lookup, uncertain results, user questions, rule-scope consent and result counts | Done | Fail. It does not state that an unanswered question leaves the transaction unchanged and unresolved, as TAG-006 requires. Actual web-search privacy remains Not Verified because the skill was not installed or run. | Add explicit wording; do not install or use web |
| T2-04 | `README.md`, `skills/CATALOG.md`, `test_distribution.py` | Check listing and distribution of the new skill | Done | Pass. Focused distribution tests passed. | — |
| T2-05 | Test environment and scope | Run focused tests, relevant full suite and compile checks; record dependency and lint limits | Done | Focused tests: 51 passed, 63 subtests passed. `compileall` passed. Full ingestion suite: 122 passed, 12 failed, 94 subtests passed; all 12 failures require missing `defusedxml==0.7.1`. Ruff unavailable. No dependencies installed, real history opened, or web request made. | Rerun affected checks after fixes |

No code change or real history use by Tester.
