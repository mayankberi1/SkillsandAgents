# BL-009 solution design — Solution Designer checklist

Assignment DESIGN-BANK-009 r1. Backlog revision 8; BL-009 scope revision 2; requirements revision 1 approved as APR-ING-REQ-005; architecture revision 1 approved as APR-ING-ARCH-003. Queue revision 8. This assignment prepares design only; implementation is not approved.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| D1 | Approved requirements and architecture | Check TAG-001–TAG-010 and approved search/data boundaries | Done | Read requirements revision 1 and architecture revision 1 | — |
| D2 | Current implementation | Inspect actual `bank_history.py`, statement skill and existing tests | Done | Read current helper, ingestion skill and related tests | — |
| D3 | Saved data and rules | Define tagging evidence, user choices, reusable rules and links to transactions | Done | Proposed `transaction_tags` and `tagging_rules`; identified conflict with format 1/eight-table approved design | User decision needed on BL-001 design update |
| D4 | Python contracts and skill steps | Define inputs, outputs, validation and user-visible results | Done | Proposed three functions in existing history helper and skill flow | — |
| D5 | Failure and privacy cases | Cover unsafe/unavailable/unclear search, failed user answers/saves and partial success | Done | Defined safe query, unresolved state, per-transaction save and deletion/recovery checks | — |
| D6 | Proposal and coverage | Map design to TAG-001–TAG-010; record tradeoffs and approval request | Done | Saved [solution design revision 1](bank-tagging-solution.md); seeks approval for existing-history update | Coordinator presents for decision |

Read actual approved records and source files. Keep the design concise and within scope. Do not edit files, run tests or implement. State any material choice the approved inputs do not settle.

## Final handoff

Design proposal revision 3: [bank-tagging-solution.md](bank-tagging-solution.md). Coverage: TAG-001–010. Current tags go on `transactions`; one `tagging_rules` table stores reusable rules; `changes` keeps the audit. Both account-and-currency and same-currency-within-history scopes are defined. The design requires a format-2 update to existing format-1 histories, with user approval and a checked safety copy. This changes the completed BL-001 design and needs user approval before implementation. No source edits or tests.

## DESIGN-BANK-009 r2 — simplify transaction tagging storage

The user asked whether transaction tags can use existing tables and why new tables are needed. Reconsider D3. Compare: tags on `transactions` with reusable rules in a separate table; tags and rules on `transactions`; and reusable rules in existing `changes`. Prefer the fewest records that keep user-approved rule scope, query behavior, deletion and correction history clear. Update the design proposal and map the result to TAG-001–TAG-010. Do not change code or tests. The database format remains an explicit issue if its structure changes.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| E1 | Recheck existing records | Read transaction and changes table fields plus current solution revision 1 | Done | Transaction rows hold financial data; `changes` is an audit record, not a current-rule store | — |
| E2 | Compare storage options | Check tag placement, reusable-rule scope, deletion and reporting needs | Done | Current tags belong on transactions; one rules table is clearer to find and remove than rules in audit text or old transaction rows | — |
| E3 | Revise proposal | Save a simpler option with tradeoffs and exact schema change | Done | Saved [solution design revision 2](bank-tagging-solution.md): transaction tag fields, one `tagging_rules` table, `changes` audit, format 2 | — |
| E4 | Coverage and handoff | Reconcile all TAG requirements; state any decision still needed | Done | Revision 2 covers TAG-001–TAG-010 and asks for approval of the storage update; no code or tests | Coordinator presents revision 2 for approval |
| E5 | Reusable rule scope | Check whether a user can choose one-account or same-currency all-account scope under TAG-007 | Done | Both scopes are supported; account rule takes priority; a same-currency rule stays within this history and remains after one account is removed unless the user removes it | — |


## DESIGN-BANK-009 r3 — remove tag change history

The user asked to remove the separate history of tag changes and approved an update to the design. Revise the proposal: save current tags on the transaction row; keep one `tagging_rules` table for reusable rules; do not add tag changes to `changes` or another history store. Keep the existing history-format update and rule scope. Save revision 3 and ask the user to approve the full design. Do not edit code or run tests.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| F1 | Remove tag change history | Remove tag change records from storage and save steps | Done | Revision 3 stores current tags on transactions and reusable rules in one table; no separate tag-change history | — |
| F2 | Reconcile design and approvals | Check scope, format update, rule choices and exact approval request | Done | Other revision 2 choices remain; revision 3 is awaiting full design approval; no code or tests | Coordinator presents revision 3 |
