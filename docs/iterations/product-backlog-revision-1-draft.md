# Product backlog

Revision: **1 (draft)**. Date: 2026-10-24. Approval: **pending**; no item scopes approved. Approval target: revision 1, BL-001–BL-005 scope revision 1 and ranks 1–5.

Execution mode: `single`. Active item ID: none. Approved queue revision: none. Stage: discovery only; no requirements, design or implementation initiated.

## Direction and confirmed decisions

User `/backlog` request: add skills that ingest bank statements using existing document skills and analyse duplicate, unusual and recurring transactions and spending.

User discovery answers: first version supports **text PDFs and CSV/XLSX**; scanned statements are deferred. Audience: **personal bank and credit-card accounts**. Keep currencies separate.

These are distributed skills, not a banking service. Reuse existing PDF and spreadsheet skills for extraction and reporting. Source files rather than bank connections are the proposed input mechanism. Analysis skills share the ingestion result to avoid repeated extraction and inconsistent totals.

Across all analyses retain account context and separate currencies: duplicate comparisons use account/currency context, unusual-transaction baselines use relevant personal-account history within each currency, and recurring groups retain account context. Consolidated spending explicitly handles transfers and repayments.

## Ranked proposal

| ID | Rank | Title | Scope revision | Status | Stage | Dependencies |
|---|---|---|---|---|---|---|
| BL-001 | 1 | Bank statement ingestion and reconciliation | 1 | Proposed | discovery | None |
| BL-002 | 2 | Duplicate transaction review | 1 | Proposed | discovery | BL-001 |
| BL-003 | 3 | Unusual transaction review | 1 | Proposed | discovery | BL-001 |
| BL-004 | 4 | Recurring transaction analysis | 1 | Proposed | discovery | BL-001 |
| BL-005 | 5 | Spending and cash-flow analysis | 1 | Proposed | discovery | BL-001 |

### BL-001 — Bank statement ingestion and reconciliation

- Problem: PDF tables and bank exports vary; unverified extraction undermines all analysis.
- Intended outcome/scope: one reusable ingestion skill using existing `pdf`/`xlsx` capabilities for supplied text PDFs and CSV/XLSX from personal bank and credit-card accounts. Preserve source/page/row, raw description, account alias, dates, signed amount and currency, distinguishing unknown values. Flag extraction uncertainty, overlapping periods and reconciliation differences; identify unavailable balances rather than claiming reconciliation. Recognise scanned inputs as unsupported in this version. Keep currencies separate.
- Rationale/evidence: local PDF and XLSX skills already cover extraction/import; E1 and E3 support traceability and minimisation. Shared ingestion prevents divergent analysis totals.
- Open questions: representative banks/countries/layouts; preferred review output. No samples supplied.
- Dependencies: none. Direct-request reference: user `/backlog`, 2026-10-24, and format/account discovery answers. Scope approval: pending.
- Lifecycle records: [Product Owner plan](iterations/bank-statement-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

### BL-002 — Duplicate transaction review

- Problem: repeat imports, overlapping statements and legitimately similar purchases can resemble duplicate charging.
- Intended outcome/scope: candidate groups with reasons and source evidence; distinguish repeat imports from possible repeated charges. Account for same-value purchases, refunds/reversals and pending/posted transitions where present. Preserve original records and uncertainty; do not silently delete or declare charges erroneous.
- Rationale/evidence: E2 documents duplicate-data causes and transaction-state changes. Inference: amount/date matches alone cannot prove duplicate charges.
- Open questions: user's preferred review output; representative ambiguous examples during later requirements.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-003 — Unusual transaction review

- Problem: unexpected charges can be hard to spot in transaction history.
- Intended outcome/scope: explainable review candidates for unusual amounts, unfamiliar merchants, unexpected fees and changes relative to available history. State comparison period and limited-history caveats; present review flags, not confirmed fraud.
- Rationale/evidence: E1 supports reviewing unknown charges. Specific anomaly signals are proposed heuristics, not validated detection performance.
- Open questions: sensitivity and minimum history to resolve during requirements; output preference.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-004 — Recurring transaction analysis

- Problem: subscriptions, bills and recurring income are obscured by variable names, amounts and timing.
- Intended outcome/scope: identify likely recurring income, bills and subscriptions with observed transactions, estimated cadence, amount changes and confidence explanations. Handle variable amounts/cadences; distinguish observations from estimated future dates.
- Rationale/evidence: E1 recommends accounting for periodic bills and reviewing unused subscriptions. No automatic cancellation or payment action proposed.
- Open questions: whether forecasts are useful; output preference.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-005 — Spending and cash-flow analysis

- Problem: transfers, refunds and credit-card repayments can distort spending totals across accounts.
- Intended outcome/scope: spending by category, merchant and period, with editable categorisation and traceable totals. Separate income, transfers, credit-card repayments, refunds and spending; expose uncertain matching. Report incomplete periods and uncategorised transactions. Keep currencies separate, without exchange-rate conversion.
- Rationale/evidence: E1 supports categorising spending. Cross-account double-counting controls are a proposed product requirement, not an existing demonstrated capability.
- Open questions: workbook, written report or both; category preferences during requirements.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24, plus personal-account/currency discovery answer. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

## Shared boundaries and proposed safeguards

No bank login/live banking integration, payments, disputes, cancellations, investment/tax advice, confirmed fraud classification, currency conversion, new installer logic or replacement document parsers. Scanned-PDF support is deferred, without a committed backlog item. Existing DOCX/PDF skills can support reports if selected.

Proposed safeguards: account aliases and minimal identifiers in outputs; synthetic examples; explicit handling of intermediate files; disclose third-party processing before transferring statement data. Do not promise local-only processing solely because extraction runs locally: runtime/model handling must also be established. These safeguards are scope proposals, not a legal-compliance certification.

## Research evidence

- **E0 — Project evidence:** [README](../README.md), [PDF skill](../skills/pdf/SKILL.md), [XLSX skill](../skills/xlsx/SKILL.md), [DOCX skill](../skills/docx/SKILL.md). PDF extraction and OCR already exist; XLSX supports tabular analysis/reporting. OCR availability does not include scans in the first-version scope. DOCX is optional reporting support.
- **E1 — Consumer workflow:** [ASIC Moneysmart: Track your spending](https://moneysmart.gov.au/budgeting/track-your-spending). Supports transaction review, categories, periodic bills, unknown charges and unused subscriptions.
- **E2 — Transaction ambiguity:** [Plaid transaction troubleshooting](https://plaid.com/docs/transactions/troubleshooting/) and [transaction states](https://plaid.com/docs/transactions/transactions-data/). Discuss duplicate-data causes and pending/posted changes. Applied by analogy to imported statements; no Plaid integration proposed.
- **E3 — Privacy/security context:** [OAIC guide to securing personal information](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/handling-personal-information/guide-to-securing-personal-information). Supports minimisation, protection and disposal/de-identification principles. Australian context is not a confirmed jurisdiction or legal applicability determination.

Research performed by Product Owner on 2026-10-24 using generic public queries. Limitations: public documentation only, no private data submitted, no bank samples supplied, no representative-layout testing, no measured extraction/detection accuracy, no legal assessment. User preferences beyond the recorded discovery answers remain unconfirmed.

## Remaining discovery questions

1. Should the main result be a reviewable Excel workbook, a written report, or both?
2. Which banks/countries should representative examples target? This can be resolved before ingestion requirements approval.

## Revision and decision history

- 2026-10-24 — Revision 1 draft: Coordinator created backlog from Product Owner DISC-BANK-001 r1 discovery. No existing backlog found; existing workflow iteration record preserved. IDs BL-001–BL-005 allocated once; earlier BL-style task IDs in that iteration record are assignment tasks, not feature IDs.
- 2026-10-24 — User confirmed text PDFs/CSV/XLSX first, scans later; personal bank/credit-card accounts; separate currencies. Incorporated before revision 1 approval proposal. No rank change.
- 2026-10-24 — Product Owner refinement DISC-BANK-001 r2 reconciled all five scopes with these answers; persisted in revision 1 draft before presentation.
- Approval pending: explicit approval of revision 1 makes only specified scopes Ready. Material revisions require a new approval proposal; downstream approvals remain separate. No feature completion claimed.
