# Product backlog

Revision: **4 (working discovery draft)**. Date: 2026-10-24. Approval: **pending**; no item scopes approved. Brainstorming continues; no formal approval requested for this working draft. Proposed baseline: BL-001 scope revision 4; BL-002–BL-005 scope revision 2; BL-006 scope revision 2; BL-007 scope revision 2; BL-008 scope revision 1; ranks 1–8. Supersedes unapproved revision 3; [revision 3 snapshot](iterations/product-backlog-revision-3-draft.md), [revision 2 snapshot](iterations/product-backlog-revision-2-draft.md) and [revision 1 snapshot](iterations/product-backlog-revision-1-draft.md) preserve history (snapshot relative links reflect their original location).

Execution mode: `single`. Active item ID: none. Approved queue revision: none. Stage: discovery only; no requirements, design or implementation initiated.

## Direction and confirmed decisions

User `/backlog` request: add skills that ingest bank statements using existing document skills and analyse duplicate, unusual and recurring transactions and spending.

User discovery answers: first version supports **text PDFs and CSV/XLSX**; scanned statements are deferred. Audience: **personal bank and credit-card accounts**. Keep currencies separate.

User expansion: save reusable data across sessions; accept statement top-ups each month; generate updated reports understandable to an ordinary person across **savings, transaction and credit-card accounts**. Monthly refresh is invoked when files are supplied; unattended schedules/notifications have not been requested.

Latest clarification supersedes any monthly-statement assumption: statements may have arbitrary or changing frequency, including custom/ad hoc exports. Coverage is based on date ranges per account, never document counts. Monthly reporting remains a possible review cadence, not an input requirement. User proposes a distributed `banker` subagent that invokes ingestion and separate Python-backed analysis/report skills, requests missing date ranges, and synthesises findings into suggested actions and an executive summary.

User now confirms: **analyse available data immediately and label gaps**, maintaining a persistent inventory for every account and date range. Completeness is not a prerequisite for analysis. User also requests projected balances and negative-balance warnings using balances and historic mortgage, bill and subscription payments.

These are distributed skills, not a banking service. Reuse existing PDF and spreadsheet skills for extraction and reporting. Source files rather than bank connections are the proposed input mechanism. Analysis skills share the ingestion result to avoid repeated extraction and inconsistent totals.

Across all analyses retain account context and separate currencies: duplicate comparisons use account/currency context, unusual-transaction baselines use relevant personal-account history within each currency, and recurring groups retain account context. Consolidated spending explicitly handles transfers and repayments.

## Ranked proposal

| ID | Rank | Title | Scope revision | Status | Stage | Dependencies |
|---|---|---|---|---|---|---|
| BL-001 | 1 | Persistent bank statement ingestion and reconciliation | 4 | Proposed | discovery | None |
| BL-002 | 2 | Duplicate transaction review | 2 | Proposed | discovery | BL-001 |
| BL-003 | 3 | Unusual transaction review | 2 | Proposed | discovery | BL-001 |
| BL-004 | 4 | Recurring transaction analysis | 2 | Proposed | discovery | BL-001 |
| BL-005 | 5 | Spending and cash-flow analysis | 2 | Proposed | discovery | BL-001 |
| BL-006 | 6 | Personal finance analysis and detailed reporting | 2 | Proposed | discovery | BL-001, BL-002, BL-003, BL-004, BL-005 |
| BL-007 | 7 | Banker subagent and executive review | 2 | Proposed | discovery | BL-001, BL-006 |
| BL-008 | 8 | Cash-balance forecasting and shortfall warnings | 1 | Proposed | discovery | BL-001, BL-004 |

### BL-001 — Persistent bank statement ingestion and reconciliation

- Problem: PDF tables and bank exports vary; unverified extraction undermines all analysis.
- Intended outcome/scope: one reusable ingestion skill using existing `pdf`/`xlsx` capabilities for supplied text PDFs and CSV/XLSX from personal bank and credit-card accounts. Preserve source/page/row, raw description, account alias, dates, signed amount and currency, distinguishing unknown values. Flag extraction uncertainty, overlapping periods and reconciliation differences; identify unavailable balances rather than claiming reconciliation. Recognise scanned inputs as unsupported in this version. Keep currencies separate.
- Scope revision 2 extension: persist reusable transaction history across sessions for savings, transaction and credit-card accounts; incrementally add monthly statements. Track imports, account identity/type, source evidence and period coverage. Repeat uploads and overlapping statements must not inflate history. Explain replacement/corrected statements and user corrections without losing lineage; mark incomplete or failed imports rather than silently treating them as complete. Include user-controlled export/deletion and recoverability expectations in later requirements; persistence location and original-file retention remain open. E4 informs retention considerations. No storage engine selected.
- Scope revision 3 supersedes monthly-input wording: accept any statement frequency and changes per account, including custom/ad hoc ranges. Track the union of verified coverage intervals separately from transaction dates. Overlaps add no extra coverage; uncertain or partial imports do not silently establish complete coverage. Infer and adapt cadence per account where evidence permits, but use it only for expectations, never as proof of coverage. Assess exact gaps within an agreed review horizon and account active dates; request the missing date range, not a particular count of files. Declared statement/export range or user confirmation supports boundaries; transaction min/max alone does not. Record covered, missing, partial/failed, uncertain and unavailable ranges distinctly. A confirmed no-activity period is not equivalent to an uploaded statement. The latest covered date is not necessarily today.
- Scope revision 4 confirms a durable inventory for each account and its date ranges, updated after each import/correction. Track coverage status and supporting sources; derive exact missing intervals within the review horizon. Expose this inventory to Banker and all analyses. User reference: immediate-analysis/account-inventory clarification, 2026-10-24.
- Rationale/evidence: local PDF and XLSX skills already cover extraction/import; E1 and E3 support traceability and minimisation. Shared ingestion prevents divergent analysis totals.
- Open questions: representative banks/countries/layouts; preferred review output. No samples supplied.
- Dependencies: none. Direct-request reference: user `/backlog`, 2026-10-24, and format/account discovery answers. Scope approval: pending.
- Lifecycle records: [Product Owner plan](iterations/bank-statement-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

### BL-002 — Duplicate transaction review

- Problem: repeat imports, overlapping statements and legitimately similar purchases can resemble duplicate charging.
- Intended outcome/scope: candidate groups with reasons and source evidence; distinguish repeat imports from possible repeated charges. Account for same-value purchases, refunds/reversals and pending/posted transitions where present. Preserve original records and uncertainty; do not silently delete or declare charges erroneous.
- Scope revision 2 extension: retain findings and user review decisions across monthly updates. New or corrected evidence may reopen a finding with an explanation; keep account/currency context and originals.
- Rationale/evidence: E2 documents duplicate-data causes and transaction-state changes. Inference: amount/date matches alone cannot prove duplicate charges.
- Open questions: user's preferred review output; representative ambiguous examples during later requirements.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-003 — Unusual transaction review

- Problem: unexpected charges can be hard to spot in transaction history.
- Intended outcome/scope: explainable review candidates for unusual amounts, unfamiliar merchants, unexpected fees and changes relative to available history. State comparison period and limited-history caveats; present review flags, not confirmed fraud.
- Scope revision 2 extension: use retained history as the baseline, distinguish new flags from reviewed findings, and disclose insufficient history. Refresh findings when corrected evidence changes the conclusion.
- Rationale/evidence: E1 supports reviewing unknown charges. Specific anomaly signals are proposed heuristics, not validated detection performance.
- Open questions: sensitivity and minimum history to resolve during requirements; output preference.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-004 — Recurring transaction analysis

- Problem: subscriptions, bills and recurring income are obscured by variable names, amounts and timing.
- Intended outcome/scope: identify likely recurring income, bills and subscriptions with observed transactions, estimated cadence, amount changes and confidence explanations. Handle variable amounts/cadences; distinguish observations from estimated future dates.
- Scope revision 2 extension: refresh recurring groups monthly, highlight price changes and newly recurring items, and flag possible missing payments with explicit uncertainty about incomplete coverage or cancellations. Recurring-cost annual estimates are optional and must state assumptions (E1).
- Rationale/evidence: E1 recommends accounting for periodic bills and reviewing unused subscriptions. No automatic cancellation or payment action proposed.
- Open questions: whether forecasts are useful; output preference.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-005 — Spending and cash-flow analysis

- Problem: transfers, refunds and credit-card repayments can distort spending totals across accounts.
- Intended outcome/scope: spending by category, merchant and period, with editable categorisation and traceable totals. Separate income, transfers, credit-card repayments, refunds and spending; expose uncertain matching. Report incomplete periods and uncategorised transactions. Keep currencies separate, without exchange-rate conversion.
- Scope revision 2 extension: update monthly and comparable historical summaries; retain category corrections. Include fee/interest totals and changes where identifiable (E5). Report unmatched transfers and coverage gaps; compare like periods or disclose differences.
- Rationale/evidence: E1 supports categorising spending. Cross-account double-counting controls are a proposed product requirement, not an existing demonstrated capability.
- Open questions: workbook, written report or both; category preferences during requirements.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24, plus personal-account/currency discovery answer. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-006 — Personal finance analysis and detailed reporting

- Problem: monthly top-ups need one understandable review of changes across accounts rather than disconnected analyses or repeatedly rebuilt history.
- Intended outcome/scope revision 1: one skill orchestrates the preceding skills when statements are added, then saves a refreshed plain-language report and report history. Explain where money went, what changed and what needs review. Include covered accounts/periods, balance as-of dates, missing inputs, source evidence and material corrections; distinguish revised reports from earlier versions. Show deposit-balance and credit-card debt trends when supported. Report format remains open; an Excel companion is proposed, not confirmed.
- Scope revision 2 supersedes the earlier orchestration boundary: a separate analysis/report skill uses accompanying Python scripts for repeatable calculations and traceable findings across BL-002–BL-005, then produces detailed reports and saved report versions. Reuse existing document skills as appropriate. Reports may cover a chosen month or other horizon regardless of input statement frequency; identify coverage limitations and qualify affected comparisons. Banker (BL-007) owns conversational coordination and executive synthesis. Proposed grouping is two skills plus Banker; backlog capabilities need not map one-to-one to skills. No script interface or storage architecture selected.
- Proposed optional use cases: savings-goal tracking against a user-supplied target and selected accounts (E6); card balance, fees/interest and statement-supplied due-date/minimum-payment review (E7); estimated upcoming recurring bills versus dated recorded funds, with missing commitments and forecast uncertainty explicit (inference from E1). No guarantee of affordability or current funds. These optional additions await user selection and are not baseline commitments until confirmed.
- Rationale/evidence: user explicitly requested monthly top-ups and updated ordinary-person reports. E1/E5–E7 support the proposed review menu; stored report lineage supports explainability after corrections.
- Open questions: plain-language report plus workbook or report alone; optional use-case priorities; history location and original-file retention.
- Dependencies: BL-001, BL-002, BL-003, BL-004, BL-005. Direct-request reference: user monthly persistence/report expansion, 2026-10-24. Scope approval: pending.
- Lifecycle records: [Monthly Product Owner plan](iterations/bank-statement-monthly-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

For BL-001–BL-005, scope revision 2 additionally references the user monthly persistence/report expansion on 2026-10-24 and the monthly Product Owner plan above. Original request references remain intact. No prior scopes were approved.

### BL-007 — Banker subagent and executive review

- Problem: users need one conversational guide to gather missing inputs, invoke repeatable analyses and explain what matters across accounts.
- Intended outcome/scope revision 1: add a distributed subagent named `banker`; it invokes ingestion/coverage and analysis/reporting skills, presents missing or uncertain date ranges, requests inputs that cover those ranges, and remembers supplied coverage. Adapt to each account's observed statement timing without requiring fixed periods or counts. Turn calculated summaries from one or more skills into a plain-language executive summary and prioritised suggested actions, with numerical claims traceable to results and source evidence.
- Scope revision 2: user confirms immediate available-data analysis with gaps labelled, rather than waiting for completeness or asking permission to proceed. Consult/update the durable account/date-range inventory; ask for missing ranges alongside results and refresh affected findings after new data arrives. Label affected comparisons and forecasts provisional or unavailable where evidence is insufficient; never invent missing transactions/balances. Present BL-008 shortfall warnings prominently when forecast results are available. User reference: immediate-analysis/account-inventory clarification and forecast request, 2026-10-24.
- Boundaries: separate facts, uncertain interpretations and optional actions. Suggested checks may concern an unfamiliar charge, recurring price change or missing data. Sending messages, disputing charges, cancelling services and moving money remain outside scope. No autonomous financial actions or schedules proposed.
- Rationale/evidence: direct user Banker brainstorming and variable-frequency/range-coverage clarification, 2026-10-24. Existing agent definitions and skill Python helpers establish repository conventions, not implemented financial capability.
- Dependencies: BL-001, BL-006. Open questions: confirm two-skill grouping; review-horizon onboarding; summary format; storage/retention and output preferences remain open. Immediate analysis and durable inventory are confirmed. Status Proposed; stage discovery; approval pending.
- Lifecycle records: [Banker Product Owner plan](iterations/banker-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

BL-001 scope revision 3 and BL-006 scope revision 2 additionally reference the Banker brainstorming and coverage clarification, 2026-10-24. All earlier approved scope remains absent; previous drafts are preserved rather than treated as approval.

### BL-008 — Cash-balance forecasting and shortfall warnings

- Problem: historic reports do not show whether payment timing could cause an upcoming shortfall in the account funding a payment.
- Intended outcome/scope revision 1: Python-backed analysis projects cash balances per funding account over an adjustable horizon, using a dated balance and expected income, mortgage payments, bills, subscriptions, card repayments, transfers and any explicit ordinary-spending allowance. Use history-based estimates and user-confirmed commitments with labelled dates, amounts and assumptions. Show first projected negative date, lowest projected balance, contributing payments and uncertainty; positive funds elsewhere must not hide an account-specific shortfall.
- Balance semantics: identify whether the starting value is statement closing, current/ledger or available balance and its as-of date. Request a fresher balance if needed; old closing balances are not current funds. Avoid counting pending payments already reflected in the starting balance, or show scenarios when uncertain. Reconcile overlapping recurring/mortgage/bill candidates so one obligation appears once. Card purchases affect debt; bank repayments affect cash. Internal transfers/card repayments are cash movements without being additional consolidated spending.
- Forecast scenarios: baseline and cautious scenarios may vary income/payment timing or variable bills. Unknown same-day posting order cannot establish precise intraday safety. Carry missing-range/account warnings, limited history, unseen commitments and stale balances into the result. Immediate analysis remains the default; if no defensible starting balance exists, return the available descriptive analysis and state that a numeric balance projection is unavailable pending input. A positive projected balance means no shortfall under stated assumptions, not guaranteed safety.
- Warning output: a prominent account-specific warning during a user-invoked review or data refresh, with drivers and suggested checks. BL-006 includes detailed forecast results; BL-007 synthesises warnings/actions. No background monitoring, scheduled notifications or automatic transfers/payment changes are included.
- Rationale/evidence: direct user forecast/alarm request, 2026-10-24; E8 supports timed cash-flow projections, E9 supports timing-shortfall context and E10 informs balance distinctions. Proposed capability within the analysis skill, not necessarily another skill.
- Dependencies: BL-001, BL-004. Open questions: default horizon (next 30 days or next payday); zero-only warning or user-selected safety buffer. Scope approval pending; status Proposed; stage discovery.
- Lifecycle records: [Forecast Product Owner plan](iterations/balance-forecast-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

## Coverage examples and proposed interaction

- One account has 1–31 January and 15 January–28 February: verified coverage is continuous 1 January–28 February; overlapping rows still require import deduplication separately.
- One statement covering the full quarter can establish that quarter without three monthly files.
- An account has 1–12 January and 20–31 January: request data covering 13–19 January, in any suitable statement/export. Do not infer zero activity.
- A quiet statement covering a month may have no transaction rows; its declared period still matters. An ad hoc export with no reliable range leaves coverage uncertain until clarified.
- Banker proposes or confirms the review horizon and expected accounts/active dates, ingests files, updates account/range inventory and immediately invokes available-data analyses. Results label exact gaps and affected conclusions while Banker requests missing ranges. New inputs refresh the inventory and analyses. It does not repeatedly request resolved ranges or treat frequency changes alone as gaps.

## Financial interpretation and report guardrails

- Transfers between owned accounts, including into savings, are not new external income or spending. Savings-account balance growth can reflect transfers and interest; it does not automatically measure newly earned savings.
- Credit-card purchases count toward spending; repayments reduce cash and card debt and must not count as spending a second time. Show unmatched or uncertain transfer links.
- Show deposit balances and card liabilities separately. Any combined position is limited to supplied accounts within each currency, not full net worth.
- Statement closing balances are dated historical values, not current available funds. Missing accounts, months and balance fields remain visible.
- Default monthly report questions: What came in and went out? Where did spending change? How did savings balances and card debt change? Which duplicate/unusual charges need review? Which bills/subscriptions changed? What data is missing?

## Shared boundaries and proposed safeguards

No bank login/live banking integration, payments, disputes, cancellations, investment/tax advice, confirmed fraud classification, currency conversion, new installer logic or replacement document parsers. Scanned-PDF support is deferred, without a committed backlog item. Existing DOCX/PDF skills can support reports if selected.

Proposed safeguards: account aliases and minimal identifiers in outputs; synthetic examples; explicit handling of intermediate files; disclose third-party processing before transferring statement data. Do not promise local-only processing solely because extraction runs locally: runtime/model handling must also be established. These safeguards are scope proposals, not a legal-compliance certification.

Durable history adds user-controlled storage-location, retention, original-file handling, export, deletion and recovery questions. Preserve category corrections and review decisions across imports; avoid unnecessary identifying details. No actual financial data is stored by this backlog work.

## Research evidence

- **E0 — Project evidence:** [README](../README.md), [PDF skill](../skills/pdf/SKILL.md), [XLSX skill](../skills/xlsx/SKILL.md), [DOCX skill](../skills/docx/SKILL.md). PDF extraction and OCR already exist; XLSX supports tabular analysis/reporting. OCR availability does not include scans in the first-version scope. DOCX is optional reporting support.
- **E1 — Consumer workflow:** [ASIC Moneysmart: Track your spending](https://moneysmart.gov.au/budgeting/track-your-spending). Supports transaction review, categories, periodic bills, unknown charges and unused subscriptions.
- **E2 — Transaction ambiguity:** [Plaid transaction troubleshooting](https://plaid.com/docs/transactions/troubleshooting/) and [transaction states](https://plaid.com/docs/transactions/transactions-data/). Discuss duplicate-data causes and pending/posted changes. Applied by analogy to imported statements; no Plaid integration proposed.
- **E3 — Privacy/security context:** [OAIC guide to securing personal information](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/handling-personal-information/guide-to-securing-personal-information). Supports minimisation, protection and disposal/de-identification principles. Australian context is not a confirmed jurisdiction or legal applicability determination.
- **E4 — Retention context:** [OAIC APP 11 guidance](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-11-app-11-security-of-personal-information). Informs retention risks and disposal of unnecessary personal information; legal applicability unassessed.
- **E5 — Balance/fee/interest review:** [Moneysmart: Track your investments](https://moneysmart.gov.au/how-to-invest/track-your-investments). Includes savings-account tracking guidance informing proposed balance, fee and interest review.
- **E6 — Savings goals:** [Moneysmart: How to start saving](https://moneysmart.gov.au/saving/how-to-start-saving). Supports setting savings goals and tracking progress; proposed optional user-target workflow.
- **E7 — Credit-card review:** [Moneysmart: Pay off your credit card](https://moneysmart.gov.au/credit-cards/pay-off-your-credit-card). Supports reviewing statements and repayment dates; proposed reporting uses stated terms rather than inferring absent information.
- **E8 — Cash-flow projection:** [CFPB cash-flow budgeting tool](https://www.consumerfinance.gov/documents/10038/cfpb_creating-cash-flow-budget_tool_2021-08.pdf). Supports starting balances, timed income/outgoings and carrying balances forward; not validation of proposed scripts.
- **E9 — Timing shortfalls:** [CFPB emergency-fund guide](https://www.consumerfinance.gov/an-essential-guide-to-building-an-emergency-fund/). Informs income/payment timing and shortfall context.
- **E10 — Balance meanings:** [Numerica actual versus available balance](https://www.numericacu.com/articles/actual-available-balance). One institution's explanation of balances/pending transactions; definitions must be established for each supplied account, not generalised across banks.

Research performed by Product Owner on 2026-10-24 using generic public queries. Limitations: public documentation only, no private data submitted, no bank samples supplied, no representative-layout testing, no measured extraction/detection accuracy, no legal assessment. User preferences beyond the recorded discovery answers remain unconfirmed.

DISC-BANK-002 expanded public-source research on the same date. No persistence/recovery trials or report-generation tests performed; evidence supports proposed user needs, not demonstrated functionality.

DISC-BANK-004 researched E8–E10 using generic public queries on 2026-10-24. No private data, forecast tests or accuracy evidence; jurisdiction-specific banking rules not assessed.

## Remaining discovery questions

1. Should saved history live in a folder the user controls or an existing personal data store, and should original statements be retained?
2. Should the plain-language monthly report also include a reviewable Excel workbook?
3. Which optional additions matter first: savings goals, recurring price changes, fee/interest review, card due dates or upcoming-bill estimates?
4. Which banks/countries should representative examples target? Resolve before ingestion requirements approval.
5. Does the proposed two-skill grouping plus Banker fit the intended experience? Should first use establish expected accounts and a review horizon, inferred where possible and confirmed when ambiguous?
6. Should the executive summary start with the most important changes and up to three evidence-backed suggested checks, followed by the detailed report?
7. Should the initial forecast horizon be the next 30 days or through the next expected payday, adjustable by the user? Warn below zero only, or additionally below a user-selected safety buffer?

Resolved: analyse immediately and label gaps; keep a persistent account/date-range inventory. Do not ask the user again whether to wait for complete data.

## Revision and decision history

- 2026-10-24 — Revision 1 draft: Coordinator created backlog from Product Owner DISC-BANK-001 r1 discovery. No existing backlog found; existing workflow iteration record preserved. IDs BL-001–BL-005 allocated once; earlier BL-style task IDs in that iteration record are assignment tasks, not feature IDs.
- 2026-10-24 — User confirmed text PDFs/CSV/XLSX first, scans later; personal bank/credit-card accounts; separate currencies. Incorporated before revision 1 approval proposal. No rank change.
- 2026-10-24 — Product Owner refinement DISC-BANK-001 r2 reconciled all five scopes with these answers; persisted in revision 1 draft before presentation.
- 2026-10-24 — Revision 2 draft: user expanded scope to durable history, monthly top-ups and refreshed personal reporting across savings, transaction and card accounts. Product Owner DISC-BANK-002 r1 refined BL-001–BL-005 to scope revision 2; Coordinator allocated BL-006 scope revision 1 at rank 6. Earlier ranks retained; exact unapproved revision 1 archived. No active work or approval invalidated because none existed.
- 2026-10-24 — Revision 3 working draft: user proposed Banker, separate Python-backed analysis/reporting and executive synthesis, then clarified arbitrary/changing statement frequency with date-range coverage as the criterion. Product Owner DISC-BANK-003 r1 refined boundaries and interval semantics. Coordinator retained existing IDs/ranks and allocated BL-007 at rank 7; BL-001 advanced to scope revision 3 and BL-006 to scope revision 2. Exact r2 draft archived. No code or skills implemented.
- 2026-10-24 — Revision 4 working draft: user requested projected balances/negative-balance alarm and confirmed immediate analysis with durable per-account/range inventory. Product Owner DISC-BANK-004 r1 researched/proposed forecast capability; Coordinator allocated BL-008 scope revision 1 at rank 8 and incorporated explicit immediate-analysis decision in BL-001 r4 and BL-007 r2. Original ranks retained; exact r3 snapshot preserved. No forecasts run or monitoring created.
- Approval pending: earlier approval proposals superseded; brainstorming continues without a formal approval demand this turn. Any eventual approval must identify the exact revision and scopes; optional additions remain unselected. Downstream approvals remain separate. No feature completion claimed.
