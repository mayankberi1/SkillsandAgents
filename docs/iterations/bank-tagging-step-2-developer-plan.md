# BL-009 step 2 — Developer checklist

Assignment DEV-TAG-IT2 r1. BL-009 scope revision 2; backlog and queue revision 8. Approved requirements APR-ING-REQ-006, architecture APR-ING-ARCH-003, solution design APR-ING-DES-005, step 1 APR-TAG-IT1-001 and step 2 APR-TAG-IT2-001. The user accepted local storage without encryption for the initial version as APR-TAG-STORE-001. Do not install skills or update a saved user history.

The Coordinator saved and acknowledged this checklist before source work. Initial inventory matches [the Coordinator plan](bank-tagging-step-2-coordinator-plan.md). Coordinator resolved the one-time user evidence question: save the accepted vendor/category/tags in the transaction, mark the applicable state as `user_confirmed`, and set `tag_source_kind='user'`; do not save raw chat text or add a history table. For reusable rules, save the user's selected rule values and evidence in `tagging_rules.evidence`. Developer must report any added, removed or unneeded file before continuing.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| DEV2-01 | Six-file baseline | Check each listed file exists or is new; record hashes/state and any mismatch with Coordinator baseline | Done | `bank_history.py` 41af18c4a314fc68eea9b67dbfb7681a1eab64aafd2d8f7b1e2c0bde14330e8a; `test_bank_history.py` 13d4ca5b526b3e013ecbf2ca55b09ea06523eda19fdb66f904bf0713c73867c1; `test_distribution.py` eff6d0a39f1fb8130456db26d7365e14d800b808291dc1048ceaa9e23b1eeadc; `README.md` e72306bcbb9b99cfc9d8079e76a3908fd7aeead105f841c50f5fdf973ca923e1; `skills/CATALOG.md` 8c290205f06f8d308e13c7159f0022a2d0a7ae5a267e04cef6c07a0547e5a38d. New `skills/bank-transaction-tagging/SKILL.md` is absent. Inventory matches Coordinator plan. | — |
| DEV2-02 | TAG-001–010 / approved design | Trace schema fields and callers; map read/tag-save/rule-save design to existing helper patterns; flag design gaps before edit | Done | Format 2 rows already store tag/source/status fields; `tagging_rules` has account/currency scope; `read_history` returns accepted rows; `_connect` provides checked transaction boundaries. Distribution tests need a new skill assertion. One-time user evidence interpretation is recorded in the Coordinator plan. | — |
| DEV2-03 | `bank_history.py` | Add minimal transaction/rule reads and safe tag/rule writes with account/currency checks; preserve all financial data; handle per-item errors without partial writes | Done | Added `read_tagging_data`, `save_tagging_result`, and `save_tagging_rule`. Preserves user-confirmed values and existing tags when omitted. | — |
| DEV2-04 | `test_bank_history.py` | Add behavioral tests for precedence-supported persistence, validation, account/currency boundaries, financial-field preservation, and failure behavior | Done | Generated-data tests cover user-tag persistence, financial-field preservation, rule replacement/application, currency scope and invalid inputs. Focused test set passed with 51 tests and 63 subtests. | — |
| DEV2-05 | New `skills/bank-transaction-tagging/SKILL.md` | Add frontmatter and concise flow for transaction choice > exact account/currency rule > exact same-currency rule > safe web lookup; uncertainty/user confirmation; save scope; separate saved/failed/unresolved results; privacy limits | Done | New skill states rule order, safe search limits, user questions, save scope and separate result states. | — |
| DEV2-06 | `README.md` and `skills/CATALOG.md` | Add the skill to existing catalog/install-facing documentation using current conventions | Done | New skill is listed in README and catalog. | — |
| DEV2-07 | `test_distribution.py` | Update/add distribution assertion only if required for the new skill; keep test scope minimal | Done | Distribution test checks new skill frontmatter, tool names, privacy rules, result states and catalog entries. | — |
| DEV2-08 | Verification and handoff | Run focused tests and compile/check available; inspect scope; report changed files, evidence, limits and review handoff | Done | Focused history and distribution tests: 51 passed, 63 subtests passed. `compileall` passed. Full ingestion suite: 121 passed, 12 failed because `defusedxml==0.7.1` is absent; 94 subtests passed. Ruff unavailable. No dependencies installed, web requests made, or real history opened. Independent reviews remain. | — |

No web request, dependency install, skill install, or real-history access/update is planned.

## Initial changed files and hashes

These values describe the implementation before independent findings and fixes. Later changes invalidate these hashes and related checks.

- `skills/bank-statement-ingestion/scripts/bank_history.py` — `1fc8aeb0b30a08484e6eea4424a4669cc744aae124d0e4b97d9da4f89b1647af`
- `tests/bank_statement_ingestion/test_bank_history.py` — `efa6450dc51c2e71390c20703bfe51a57e12d62ba15deddfeb76a690696b9fca`
- `tests/bank_statement_ingestion/test_distribution.py` — `eeee725554712f3d5cf3e9c5c30cf8283e42804767f751fbac1cc6ccf2e8229d`
- `skills/bank-transaction-tagging/SKILL.md` — `c68ff1b42611772b6e3e6e5f90ac145120d8a9394b7b1edf758878fd3969b60b`
- `README.md` — `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae`
- `skills/CATALOG.md` — `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91`. Developer confirmed earlier hash was a transcription error; catalog did not change after tests.

## Current files after remediation

Security-fix assignment DEV-TAG-IT2-SEC-FIX r1 changed only the helper, the two tests and the tagging skill. Coordinator independently verified these current hashes on 5 November 2026:

- `skills/bank-statement-ingestion/scripts/bank_history.py` — `7ab6fbf3adf1182a77514cc74be742dd12fd1b45f607e8dbf0399952b4c00a6b`
- `tests/bank_statement_ingestion/test_bank_history.py` — `1bc57309c09fcd9bc80a77d5b9febc8ef55e7b7f571ecefef209d64334dff6a0`
- `tests/bank_statement_ingestion/test_distribution.py` — `777c7c009d39c076f669cdcd09bd690fe406bfb6e9e113ce13b27c5c26b593f3`
- `skills/bank-transaction-tagging/SKILL.md` — `4a55ed5f0531293112a260695e7370962d1e097ca4461c3721ef4757c02ec57d`
- `README.md` — `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae`
- `skills/CATALOG.md` — `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91`

The Developer's security-fix run passed 56 focused tests and 76 subtests; compile passed. Independent rechecks remain required.

## Current files after bounded reads

Assignment DEV-TAG-IT2-READ-FIX r1 changed only the history helper, the history tests, distribution test and tagging skill. Coordinator verified the final hashes on 5 November 2026:

- `skills/bank-statement-ingestion/scripts/bank_history.py` — `196700603502dbb31646aacc8a6a38dc63a5cb767b85f62063b3880d2d16c91b`
- `tests/bank_statement_ingestion/test_bank_history.py` — `03154fff6567a99efbfcf1325929d31381ffb713f9fa80d4e6813006146c1a4c`
- `tests/bank_statement_ingestion/test_distribution.py` — `c7355f8a289edf7d3bb6e480c5026e54af353467beaeaf5f53c78092dd11cf3e`
- `skills/bank-transaction-tagging/SKILL.md` — `19912a7d70e02aa8e88994570a01a0825912ca6258974362c584a41249687e61`
- `README.md` — `c67b8f961e2478a8ccf14a6652a32d2486e5927011c53167c75238c750e11fae`
- `skills/CATALOG.md` — `376e5e2f0f646bfc8517b94f328e175cbd390178c34624cca5d39628f0b42e91`

Developer's focused run: 57 tests and 85 subtests passed; compile passed. No full ingestion test run was made after pagination. Independent rechecks remain.
