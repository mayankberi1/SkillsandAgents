# BL-009 — Implementation steps

Revision 1. Date: 4 November 2026. **Status: step 1 awaits approval.** BL-009 scope 2; backlog and queue revision 8. Requirements revision 2 is approved as APR-ING-REQ-006. Architecture revision 1 is approved as APR-ING-ARCH-003. Solution design revision 3 is approved as APR-ING-DES-004. BL-001 is Done.

## Proposed steps

| Step | Goal and requirements | Files | Main checks |
|---|---|---|---|
| **1 — Saved tags and safe history update** | Add current vendor/category/tags to transaction rows and add `tagging_rules`. Add a user-approved update from history format 1 to 2. TAG-001, 002, 007–010. | `skills/bank-statement-ingestion/scripts/bank_history.py`; `tests/bank_statement_ingestion/test_bank_history.py`; `tests/bank_statement_ingestion/test_maintenance.py`; `skills/bank-statement-ingestion/SKILL.md`; `docs/iterations/bank-ingestion-solution.md` | New histories use format 2. Format 1 stays unchanged until the user agrees to update it. Before update, make and check a full copy. On failure, keep format 1 usable. Preserve transaction IDs and financial fields. Save only current tags and source; no tag-change history. Include new fields/rules in export, restore and deletion checks. |
| **2 — Tag transactions** | Add read/save functions and skill steps for rule matching, safe vendor search, user questions and report of results. TAG-001–010. Requires step 1 and separate approval. | `skills/bank-statement-ingestion/scripts/bank_history.py`; `tests/bank_statement_ingestion/test_bank_history.py`; new `skills/bank-transaction-tagging/SKILL.md`; `README.md`; `skills/CATALOG.md`; distribution tests as needed | Transaction choice before account rule, account rule before same-currency rule, then web search. Keep currencies separate. Send only a safe business name. Ask the user when a result is unclear. Report saved, failed and unresolved items. Do not change financial fields or mark a vendor suggestion as a confirmed category. |

## Step 1 tests and reviews

- Test a new format-2 history and a format-1 update using generated local data.
- Check backup contents before and after update; check declined and failed updates leave the original usable.
- Check tag fields and rules survive export and restore, and deletion removes only selected records and rules.
- Check no earlier tag values are kept. Existing financial fields and transaction IDs stay unchanged.
- Run the focused tests, relevant full test suite, compilation and available lint checks.
- Independent Tester, Code Reviewer and Security Reviewer check the changed files and update behavior. Save their plans and results before marking step 1 complete.

Step 1 adds and tests the update path. It does not run the update on any user history. The installed skill must ask for clear user approval before each format-1 history update. Step 2 cannot start until step 1 passes and receives its own approval.

## Approval request

Approve step 1 only: saved tag fields and reusable rules, safe format-1 to format-2 update support, listed files, tests and independent reviews. This does not approve code changes yet; it authorizes the Developer to implement step 1 after approval. It does not approve running an update on a real history, step 2, release or installation.
