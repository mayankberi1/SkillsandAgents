# BL-009 — Transaction tagging lifecycle

Lifecycle revision 2. Date: 5 November 2026. Backlog revision 8. Execution mode: queue. BL-009 scope revision 2 is complete. No item is active; the next item has not been selected.

| Record | Current state |
|---|---|
| Backlog item | BL-009, rank 2, Done |
| Scope approval | APR-BANK-008 approved scope revision 2 |
| Dependency | BL-001 Done; completion evidence in [BL-001 coordinator record](bank-ingestion-step-3-coordinator-plan.md) |
| Queue selection | PLAN-QUEUE-001 r1 selected BL-009 as the highest-ranked eligible Ready item |
| Requirements | Revision 1 approved as APR-ING-REQ-005; revision 2 approved as APR-ING-REQ-006; it removes tag-change history |
| Architecture | Revision 1 approved as APR-ING-ARCH-003, option A |
| Implementation | Steps 1 and 2 are complete under APR-TAG-IT1-001 and APR-TAG-IT2-001 |
| Next action | No queue item was started. `/next` can select the next eligible item. |

The approved scope covers local saved tags, privacy-minimised vendor lookup, user classification when lookup fails, and reusable user-approved tagging rules. Requirements must clarify category choices, review thresholds and names that may identify individuals. Do not change the approved scope or rank. Queue processing may continue only through separately approved stages.

## Step 2 completion — 5 November 2026

The Developer completed the approved tagging functions, separate skill and catalog references. The final fix validates page cursors, preserves account/date filters on each page and limits rule reads to 200 applicable rules. Independent Tester, Code Reviewer and Security Reviewer r4 passed. Focused tests passed: 60 tests and 92 subtests; Python compilation passed. A separate generated check confirmed that 200 matching rules succeed and 201 raises a clear error. The wider ingestion test run had 12 XLSX failures because `defusedxml==0.7.1` is missing; no dependency was installed. Ruff is unavailable. No real history was opened or changed, and the skills were not installed into a user harness. See the [step 2 Coordinator checklist](bank-tagging-step-2-coordinator-plan.md) and the [Tester](bank-tagging-step-2-tester-plan-r4.md), [Code Reviewer](bank-tagging-step-2-code-reviewer-plan-r4.md) and [Security Reviewer](bank-tagging-step-2-security-reviewer-plan-r4.md) records.

BL-009 is Done for the approved code scope. No later queue item or installation/use task was started.

## Requirements revision 1 — approved

Product Owner REQ-BANK-009 r1 completed requirements revision 1. The user approved it without changes. It defines three owners (BL-001, BL-009 and BL-010), the user flow, privacy rules, failure behavior and TAG-001–TAG-010. It proposes common plus custom categories, vendor-only labels when purchase details are unknown, and a clear public source before suggesting one business match. No data fields, web service, command interface or implementation was selected. Architecture review is next.

## Approval — 4 November 2026

The user replied “approved”. Coordinator recorded APR-ING-REQ-005 for requirements revision 1, TAG-001–TAG-010 and the three proposed defaults. No text changed. BL-009 advanced to architecture. The Architect must assess applicable web lookup and privacy boundaries and return an architecture proposal. No design or implementation approval.

## Architecture revision 1 — approved

Architect ARCH-BANK-009 r1 compared runner web search with a controlled provider helper. The user approved option A without changes as APR-ING-ARCH-003. The tagging skill uses approved search when available and sends only a safe business name. Results remain vendor suggestions with source and uncertainty; categories and reusable rules need user confirmation. If search is unsafe, unavailable or unclear, ask the user. No schema, code or tests were selected. See [architecture revision 1](bank-tagging-architecture.md).

## Approval — 4 November 2026

The user replied “approved” to architecture revision 1, option A. Coordinator recorded APR-ING-ARCH-003 without changing the proposal. BL-009 advanced to solution design. Implementation remains unapproved.

The Solution Designer's initial checklist is saved at [the solution design plan](bank-tagging-solution-designer-plan.md). The solution designer will define data records, Python functions, skill steps and failure behavior from the approved requirements and architecture. No source changes or tests are authorized yet.

## Solution design revision 3 — approved

After the user asked why tags need a separate table, the Solution Designer revised the proposal. Current tags go on each transaction row. One `tagging_rules` table stores reusable rules. The design does not keep a separate history of tag changes. The design supports a rule for one account and currency, or for all accounts in this history with one currency. Account rules take priority. A same-currency rule remains if one account is removed, unless the user removes the rule during review.

This still changes BL-001's approved format 1: the transaction table gains fields and the database gains one table. The proposal defines format 2 and a user-approved update. [Solution design revision 3](bank-tagging-solution.md) is approved as APR-ING-DES-004. No code or tests have changed.


The user approved solution design revision 3. Coordinator recorded APR-ING-DES-004. During approval reconciliation, the Coordinator found that approved requirements revision 1 says to keep tag changes. The Coordinator saved requirements revision 2 to remove this conflict and preserve revision 1. The user approved requirements revision 2 as APR-ING-REQ-006. Coordinator set BL-009 In Progress at iteration planning and saved [implementation steps revision 1](bank-tagging-iterations.md). The user then directed that history updates use one database transaction without a separate copy. The Coordinator saved design revision 4 and iteration plan revision 2. The user approved design revision 4 as APR-ING-DES-005 and step 1 as APR-TAG-IT1-001. Step 1 passed independent tests and code and security reviews. The user approved step 2 as APR-TAG-IT2-001 and accepted local storage without encryption for the initial version as APR-TAG-STORE-001. No real history was opened or changed. Step 2 implementation is in progress; it does not permit installation or use on a saved history.


## Iteration plan — revised after transaction update direction

The plan splits BL-009 into two steps. Step 1 adds saved tag fields and reusable rules and tests a format update that commits all changes together or rolls all changes back. Step 2 adds the tagging skill and result flow. Each step needs separate approval. See [implementation steps revision 2](bank-tagging-iterations.md).


## Step 1 implementation — APR-TAG-IT1-001

The user approved step 1 of [implementation plan revision 2](bank-tagging-iterations.md). The scope includes transaction tag fields, `tagging_rules`, a format-1 to format-2 update in one database transaction, and tests. It does not permit an update to a real history or step 2. Coordinator saved [the step 1 coordinator checklist](bank-tagging-step-1-coordinator-plan.md); [Developer checklist](bank-tagging-step-1-developer-plan.md) is saved and acknowledged before source work.
