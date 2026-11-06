# BL-009 step 2 — Coordinator checklist

Assignment COORD-DEV-TAG-IT2 r1. Backlog revision 8; BL-009 scope revision 2; queue revision 8. Requirements APR-ING-REQ-006, architecture APR-ING-ARCH-003 and solution design APR-ING-DES-005 are approved. Step 1 APR-TAG-IT1-001 is complete. The user approved step 2 as APR-TAG-IT2-001 and accepted local storage without encryption for the initial version as APR-TAG-STORE-001. Do not install skills or update a saved user history.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| CO1 | Approval and baseline | Confirm exact approved scope, file inventory and current source state | Done | Scope is implementation step 2 in [implementation plan revision 3](bank-tagging-iterations.md). See baseline list below. | — |
| CO2 | Developer checkpoint | Obtain Developer's checklist before source edits; acknowledge it | Done | Saved and acknowledged [Developer checklist](bank-tagging-step-2-developer-plan.md). Five existing source/doc files have baseline hashes; the new tagging skill is absent as expected. | Developer may trace and implement within approved scope |
| CO3 | Implementation and acceptance | Reconcile work to TAG-001–010 and the approved design | Done | Final focused run: 60 passed and 92 subtests; compile passed. Tester, Code Reviewer and Security Reviewer r4 passed. Generated boundary check: 200 matching rules succeed; 201 raises an error. Full ingestion suite: 131 passed; 12 XLSX failures need missing `defusedxml==0.7.1`. `ruff` is unavailable. See the r4 records below. | No real history was used; no skills installed |
| CO4 | Completion or blocker | Record results and next approval state | Done | Step 2 implementation is complete under APR-TAG-IT2-001. No source scope remains. | Keep actual skill installation or use on saved data separate; this work did not do either |

## Approved step 2 scope

- Add functions to read transaction and rule data, save a tag result, and save a reusable rule.
- Add a separate skill for rule matching, privacy-limited vendor search instructions, user classification questions, saving confirmed results and clear result reporting.
- Apply a transaction-specific choice first, then an exact account-and-currency rule, then an exact same-currency all-account rule, then web lookup.
- Keep unsafe or unclear vendor names out of web search. Do not send amounts, dates, account/card details, personal names or references.
- Keep currency and account boundaries. Do not change transaction dates, amounts, currencies, account/card links, or identify transfers/card payments.
- Report saved, failed and unresolved items separately. Continue safe work when one item fails.
- Do not add encryption in this step. The user accepted local storage without encryption for the initial version.
- Coordinator implementation interpretation for TAG-007: a one-transaction user answer is saved as the current vendor/category/user tags, with the relevant `user_confirmed` status and `tag_source_kind='user'`. Do not save the raw chat text or add another history table. For a reusable rule, save the selected rule values and user evidence in `tagging_rules.evidence`. This uses the approved current-value fields and does not add tag-change history.
- Do not install the skill or update saved user data.

## Baseline inventory

- `skills/bank-statement-ingestion/scripts/bank_history.py`
- `tests/bank_statement_ingestion/test_bank_history.py`
- `tests/bank_statement_ingestion/test_distribution.py`
- `skills/bank-transaction-tagging/SKILL.md` (new)
- `README.md`
- `skills/CATALOG.md`

Developer must report any added, removed or unneeded file before work continues. Tests must use generated local data. No web request is required for implementation; the new skill may direct the user agent to use an approved web-search tool at run time.

## Independent review checkpoints

- [Tester checklist](bank-tagging-step-2-tester-plan.md), TEST-TAG-IT2 r1. Awaiting confirmation.
- [Code Reviewer checklist](bank-tagging-step-2-code-reviewer-plan.md), REVIEW-TAG-IT2 r1. Initial plan and six-file hash inventory confirmed; Coordinator acknowledgement recorded below.
- [Security Reviewer checklist](bank-tagging-step-2-security-reviewer-plan.md), SEC-TAG-IT2 r1. Initial plan and accepted local-storage choice confirmed; Coordinator acknowledgement recorded below.

### Reviewer checkpoints

- Code Reviewer confirmed the six-file inventory and hashes on 5 November 2026. Coordinator acknowledged the checkpoint; substantive review may proceed.
- Security Reviewer confirmed all six files, data-flow scope and accepted local-storage choice on 5 November 2026. Coordinator acknowledged the checkpoint; substantive review may proceed.
- Code review verdict is Fail pending two fixes. Tester found two additional issues. See [fix checklist](bank-tagging-step-2-developer-fix-plan.md). Step 2 is not complete.
- Security review verdict is Fail pending remediation. See [security fix checklist](bank-tagging-step-2-security-fix-plan.md). The review snapshot overlapped Developer edits; it does not replace the required review of stable final files.
- Developer completed security fixes and saved stable hashes in [security Developer checklist](bank-tagging-step-2-security-developer-plan.md). The Coordinator verified them. New revision 2 checklists are saved: [Code Reviewer](bank-tagging-step-2-code-reviewer-plan-r2.md), [Tester](bank-tagging-step-2-tester-plan-r2.md) and [Security Reviewer](bank-tagging-step-2-security-reviewer-plan-r2.md). All three reviewers confirmed their plans; Coordinator acknowledged the checkpoints on 5 November 2026.
- Tester confirmed TEST-TAG-IT2 r2 and will run generated-data checks. Coordinator saved and acknowledged the checkpoint; testing may proceed.
- Tester r2 passed the available step-2 checks, with the `defusedxml` limit recorded. Code Reviewer r2 passed and found no new defect. Security Reviewer r2 failed only on unbounded reads; see the bounded-read plan.

- Saved bounded-read re-review checklists: [Tester r3](bank-tagging-step-2-tester-plan-r3.md), [Code Reviewer r3](bank-tagging-step-2-code-reviewer-plan-r3.md), and [Security Reviewer r3](bank-tagging-step-2-security-reviewer-plan-r3.md). These reviews found issues, recorded in those files.
- Tester confirmed TEST-TAG-IT2 r3. Coordinator saved and acknowledged the checkpoint; bounded-read tests may proceed.
- Security Reviewer confirmed SEC-TAG-IT2 r3. Coordinator saved and acknowledged the checkpoint; review may proceed.
- Code Reviewer confirmed REVIEW-TAG-IT2 r3 and current hashes. Coordinator saved and acknowledged the checkpoint; review may proceed.
- Tester r3 failed malformed cursor handling; Code Reviewer r3 failed because later pages can lose account/date filters; Security Reviewer r3 failed because applicable rules are read and returned without a bound. Findings and evidence are recorded in the r3 review files. Step 2 remains open.
- Next fix scope: validate cursor type, format, existence and selected scope; tell the skill to repeat the same filters and page limit on every page; query only rules for the selected page accounts and currencies and reject more than 200 applicable rules rather than silently dropping rules. Add regression tests. No schema change, real history, install or web use.
- Coordinator saved the initial [read safety fix checklist](bank-tagging-step-2-read-fix-plan.md) and Tester r4 checklist (below) with fresh hashes. Tester confirmed the checklist and baseline; Coordinator acknowledges it. Testing may start only after the Developer completes the fix.
- Coordinator also saved and acknowledged the [Code Reviewer r4 checklist](bank-tagging-step-2-code-reviewer-plan-r4.md) with the same six-file baseline. Reviewer may assess only stable final files after implementation.
- Coordinator saved and acknowledged the [Security Reviewer r4 checklist](bank-tagging-step-2-security-reviewer-plan-r4.md) with the same six-file baseline and accepted storage choice. Review may start after stable implementation.
- Developer completed [read safety fixes](bank-tagging-step-2-read-fix-plan.md); all six hashes are recorded and verified. Focused tests passed: 60 tests and 92 subtests; compile passed. Coordinator confirms only the approved helper, tests and tagging skill changed. Independent r4 checks may start. Full ingestion suite and style check were not run.
- Code Reviewer r4 passed with no actionable defect; see [Code Reviewer r4](bank-tagging-step-2-code-reviewer-plan-r4.md).
- Security Reviewer r4 passed with no finding; see [Security Reviewer r4](bank-tagging-step-2-security-reviewer-plan-r4.md). The review noted that paging scope relies on the skill instruction and that the checked-in tests did not directly cover exactly 200 rules. The Tester later ran that boundary as a separate generated-data check.
- Tester r4 passed. Focused tests: 60 passed, 92 subtests; compile passed. Separate generated check confirms exactly 200 rules succeed and 201 fails clearly. Full ingestion suite: 131 passed, 12 XLSX failures caused by missing `defusedxml==0.7.1`; no install was made. See [Tester r4](bank-tagging-step-2-tester-plan-r4.md). All three independent r4 reviews now pass; the wider-suite dependency limit remains recorded.
- `ruff check` could not run because `ruff` is not installed. No package was installed. No real history was opened or changed, and neither skill was installed into a user harness.
