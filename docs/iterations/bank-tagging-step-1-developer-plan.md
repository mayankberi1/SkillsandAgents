# BL-009 step 1 — Developer checklist

Assignment DEV-TAG-IT1 r1. Backlog revision 8; BL-009 scope revision 2; queue revision 8. Requirements APR-ING-REQ-006, architecture APR-ING-ARCH-003, design APR-ING-DES-005 and step approval APR-TAG-IT1-001 apply. Step 1 only. Do not update a real history or start step 2.

The developer inspected the approved requirements, design, iteration plan and target file list. No files were changed during the initial check. Source hashes and test results must be recorded before and after implementation.

## Agreed implementation details

These details implement the approved design. They do not change its behavior:

- Add nullable current values on `transactions` for vendor, category, source link/title, lookup date, uncertainty, source kind and matching rule ID.
- Add vendor and category state fields with safe `unknown` defaults. Use `suggested`, `user_confirmed` and `rule_confirmed` only where they apply.
- Store user tags as a JSON list. Do not store earlier tag values.
- `tagging_rules` stores current rules only: ID, optional account ID, currency, exact normalized match, vendor/category/tags, user evidence, active state and dates.
- A rule with no account ID applies to all accounts in this history with its currency. Account-specific rules apply only to their account. If matching rules disagree, leave the transaction unresolved for the user.
- The format update function must require an explicit `user_approved=True` input. Reject any other value before changing the database. The skill asks the user before it passes true.
- Use one write transaction for all new fields, the rules table and format number. Check the result before commit. On any error, issue rollback and confirm the database remains at format 1.

## Tasks

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| S1-01 | Approved requirements and source baseline | Recheck scope and record source/test hashes | Done | Initial read completed; record hashes before source changes | — |
| S1-02 | `skills/bank-statement-ingestion/scripts/bank_history.py` | Add format 2 fields, rules table, explicit transactional update, named-column transaction inserts and checked rule deletion | Done | Added format 2 schema, user-approved one-transaction update with rollback confirmation, and shared-rule choices checked against reviewed effects | Tests and review remain |
| S1-03 | History update failure behavior | Test success, declined update and injected failures at each change | Done | Tests inject failures after table creation, each added column, format-number change and schema check; they confirm rollback and unchanged format-1 schema. Success keeps transaction IDs and financial fields. | — |
| S1-04 | `tests/bank_statement_ingestion/test_bank_history.py` | Test fields, rules, user approval and unchanged financial records | Done | Generated format-1 history updates to format 2; refusal and non-true approvals leave it unchanged | — |
| S1-05 | `tests/bank_statement_ingestion/test_maintenance.py` | Test export, restore and deletion of rules and tagged transactions | Done | Tag fields and rules survive export/restore; account choices remove or keep shared rules; account-specific and full-history rules delete as planned | — |
| S1-06 | `skills/bank-statement-ingestion/SKILL.md` | Require user approval for each existing-history update; state format 2 | Done | Skill checks the saved format, asks before update, and explains keep/remove choices for shared rules during account deletion | — |
| S1-07 | `docs/iterations/bank-ingestion-solution.md` | Reconcile BL-001 design record to format 2 and transactional update | Done | Records format-2 tag fields, `tagging_rules`, and one-transaction update behavior | — |
| S1-08 | `tests/bank_statement_ingestion/test_distribution.py` | Update the installed-copy format assertion and check skill instructions | Done | Added after baseline search found an assertion tied to format 1; installed-copy test expects helper 1/database format 2 | — |
| S1-09 | Checks and handoff | Run focused/full tests, compilation, lint if available; inspect exact changed files | Done | Focused history, maintenance and distribution tests: 97 passed, 70 subtests passed. `compileall` passed. Full ingestion test run: 118 passed, 12 failed because `defusedxml==0.7.1` is absent. Full repo collection is blocked by missing `google-auth` and `google-api-python-client`. Ruff is unavailable. Independent Tester, Code Reviewer and Security Reviewer completed. | No dependency was installed; no saved data was used |

Baseline hashes before source changes: `bank_history.py` 79e31e57121e4f40b689dca274a17f4b06ff3b1adf6078b03d0d871de1123d31; `test_bank_history.py` 27cad6bd5b103ee6fe5c7610538dd31f9225278e3dea3ac06386467c35e5db32; `test_maintenance.py` aa64c69f40edb90541848f847b0e73aec304de4dbfb822df604b999582d32af8; `SKILL.md` 51d2b1c757c77e3390abaa862edc6e888a0a7cf59f085975f3348120917ba493; `bank-ingestion-solution.md` 4ee51f7e56d51bf8cabd7691617bc260afc8dbbb247cd52460f56ed40403a5f.

No real history has been opened or updated. The deletion choice is defined by Coordinator: preview same-currency shared rules, ask keep/remove for each, then recheck IDs and choices at execution; remove account-specific rules with the account and all rules with full-history deletion. Final source hashes and test results are recorded in the handoff.

## Changed files and final hashes

- `skills/bank-statement-ingestion/scripts/bank_history.py` — `41af18c4a314fc68eea9b67dbfb7681a1eab64aafd2d8f7b1e2c0bde14330e8a`
- `tests/bank_statement_ingestion/test_bank_history.py` — `13d4ca5b526b3e013ecbf2ca55b09ea06523eda19fdb66f904bf0713c73867c1`
- `tests/bank_statement_ingestion/test_maintenance.py` — `e87104f63b14e4689ebcb888a77ca60e8592fc668de1811dde726b1358924b72`
- `tests/bank_statement_ingestion/test_distribution.py` — `eff6d0a39f1fb8130456db26d7365e14d800b808291dc1048ceaa9e23b1eeadc` (added after the baseline search found its database-format assertion)
- `skills/bank-statement-ingestion/SKILL.md` — `07cbb82fa36587a747c453839bf409a40368421b4e1c74dbf88a5c909748fd11`
- `docs/iterations/bank-ingestion-solution.md` — `d5f3ba047b17cd8fc3b18a1969b40ea2c8c0c7b08a8ff81d9de8febad98375cc`

Coverage check: six implementation files were changed or checked as required. `test_distribution.py` was necessary because its installed-copy check expected database format 1. No step 2 files, real histories, installer files or external services were changed. The independent Code Reviewer found no actionable defect. The Security Reviewer passed current content and noted no encryption at rest. The Tester confirmed the focused results and the wider-suite limit. Before-state hashes exist for five files; no before hash exists for `test_distribution.py`, so its diff could not be verified by hash.

## Coordinator decision: account deletion

For account deletion, show each history-wide same-currency rule and require an explicit keep-or-remove choice. Check the same rule IDs and choices again at execution; if they changed, stop and ask for a new review. Remove account-specific rules with the account. Full-history deletion removes all rules. This follows the approved design and is not a scope change.
