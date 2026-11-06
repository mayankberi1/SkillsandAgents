# BL-009 — Implementation steps

Revision 4. Updated 5 November 2026. **Steps 1 and 2 are complete.** Step 1 approval APR-TAG-IT1-001. Step 2 approval APR-TAG-IT2-001, user reply “approved to proceed”. The user also approved local storage without encryption for the initial version as APR-TAG-STORE-001. Revisions 2–3 and prior decisions remain in history. BL-009 scope 2; backlog and queue revision 8. Requirements revision 2 is approved as APR-ING-REQ-006. Architecture revision 1 is approved as APR-ING-ARCH-003. Solution design revision 4 is approved as APR-ING-DES-005. BL-001 is Done.

## Current assignment

Coordinator checkpoint: [step 1 checklist](bank-tagging-step-1-coordinator-plan.md) and [step 2 checklist](bank-tagging-step-2-coordinator-plan.md). Step 1 implementation and independent reviews are complete. The user accepted local storage without encryption for the initial version. No saved history was opened or changed.

## Proposed steps

| Step | Goal and requirements | Files | Main checks |
|---|---|---|---|
| **1 — Saved tags and safe history update** | Add current vendor/category/tags to transaction rows and add `tagging_rules`. Add a user-approved update from history format 1 to 2 using one database transaction. TAG-001, 002, 007–010. | `skills/bank-statement-ingestion/scripts/bank_history.py`; `tests/bank_statement_ingestion/test_bank_history.py`; `tests/bank_statement_ingestion/test_maintenance.py`; `skills/bank-statement-ingestion/SKILL.md`; `docs/iterations/bank-ingestion-solution.md` | New histories use format 2. Format 1 stays unchanged until the user agrees to update it. Run the whole update in one transaction. Commit only after checks pass. Roll back on failure so format 1 stays usable. Do not make a separate history copy. Preserve transaction IDs and financial fields. Save only current tags and source; no tag-change history. Include new fields/rules in export, restore and deletion checks. |
| **2 — Tag transactions — Complete** | Add read/save functions and skill steps for rule matching, safe vendor search, user questions and report of results. TAG-001–010. Approved as APR-TAG-IT2-001. | `skills/bank-statement-ingestion/scripts/bank_history.py`; `tests/bank_statement_ingestion/test_bank_history.py`; `skills/bank-transaction-tagging/SKILL.md`; `README.md`; `skills/CATALOG.md`; distribution tests | Transaction choice before account rule, account rule before same-currency rule, then web search. Keep currencies separate. Send only a safe business name. Ask the user when a result is unclear. Report saved, failed and unresolved items. Do not change financial fields or mark a vendor suggestion as a confirmed category. Paging uses a valid in-scope transaction ID, preserves filters, and caps rule results at 200 with an error above the cap. |

## Step 1 tests and reviews

- Test a new format-2 history and a format-1 update using generated local data.
- Check that one transaction commits all changes or rolls all changes back. Inject failures after each change and check the original tables, data and format number stay unchanged.
- Check tag fields and rules survive export and restore, and deletion removes only selected records and rules.
- Check no earlier tag values are kept. Existing financial fields and transaction IDs stay unchanged.
- Run the focused tests, relevant full test suite, compilation and available lint checks.
- Independent Tester, Code Reviewer and Security Reviewer check the changed files and update behavior. Save their plans and results before marking step 1 complete.

Step 1 adds and tests the update path. It does not run the update on any user history. The installed skill must ask for clear user approval before each format-1 history update. Step 2 cannot start until step 1 passes and receives its own approval.

## Approval record

The user approved step 1 as APR-TAG-IT1-001. This authorized development of saved tag fields and reusable rules, one-transaction format-1 to format-2 update support, listed files, tests and independent reviews. It did not approve running an update on a real history, step 2, release or installation.

The user approved step 2 as APR-TAG-IT2-001. This authorizes read/save functions, rule matching, the separate tagging skill, privacy-limited vendor search instructions, user questions and result reporting, tests and independent reviews for the listed files. It does not authorize installing the skills or updating any saved user history. The user accepted local storage without encryption for the initial version as APR-TAG-STORE-001. Do not add encryption in this step.

## Account deletion rule review

For account deletion, show same-currency rules that apply across the history. Require an explicit keep-or-remove choice for each rule. Check the rule IDs and choices again before deletion; if they changed, stop and show a new review. Remove account-specific rules with their account. Full-history deletion removes all rules.

## Test file found during step 1

The baseline check found that `tests/bank_statement_ingestion/test_distribution.py` assumes the database format number equals the helper version. Step 1 changes only the database format number, so the test now checks helper version 1 and database format 2. This test-only file was added to the step 1 review inventory; it does not add product behavior.

## Independent Tester plan

Saved [TEST-TAG-IT1 plan](bank-tagging-step-1-tester-plan.md). It checks schema update, rollback, current tags, rule deletion choices, export/restore and distribution instructions. The Developer plan lists six final files but contains a stale five-file count; the Coordinator will reconcile this before completion.

## Independent Code Reviewer plan

Saved [REVIEW-TAG-IT1 plan](bank-tagging-step-1-code-reviewer-plan.md). It checks all six implementation files, including the transactional update, account-deletion choices, simplicity and recorded test evidence.

## Independent Security Reviewer plan

Saved [SEC-TAG-IT1 plan](bank-tagging-step-1-security-reviewer-plan.md). It covers approval, rollback, paths, privacy, rule deletion, test data and per-file results. It records missing prior-file evidence for the added distribution test.

## Step 2 completion — 5 November 2026

Developer completed the approved tagging reads, saves, skill and distribution references. The last fix validates page cursors, preserves account/date filters and scopes/bounds rule reads. Independent Tester, Code Reviewer and Security Reviewer revision 4 all passed. Focused tests passed (60 tests, 92 subtests); compile passed. A generated test confirmed 200 matching rules succeed and 201 fails. The full ingestion suite had 12 XLSX failures because `defusedxml==0.7.1` is missing; no dependency was installed. Ruff was unavailable. See the [Coordinator checklist](bank-tagging-step-2-coordinator-plan.md) and r4 review plans. No real history was opened or changed. The skills were not installed into a harness.
