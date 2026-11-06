# Product backlog

Revision: **7 (working discovery draft)**. Date: 2026-10-25. Approval: **pending**; no item scopes approved. User resumed storage brainstorming; revision 6 approval proposal superseded. Current item scope revisions and ranks are in the table below; all items remain individually selectable and dependencies govern later execution. Storage discussion is conceptual, not a selected architecture/schema. [Revision 6 snapshot](iterations/product-backlog-revision-6-draft.md), [revision 5 snapshot](iterations/product-backlog-revision-5-draft.md), [revision 4 snapshot](iterations/product-backlog-revision-4-draft.md), [revision 3 snapshot](iterations/product-backlog-revision-3-draft.md), [revision 2 snapshot](iterations/product-backlog-revision-2-draft.md) and [revision 1 snapshot](iterations/product-backlog-revision-1-draft.md) preserve history (snapshot relative links reflect their original location).

Execution mode: `single`. Active item ID: none. Approved queue revision: none. Stage: discovery only; no requirements, design or implementation initiated.

## Direction and confirmed decisions

User `/backlog` request: add skills that ingest bank statements using existing document skills and analyse duplicate, unusual and recurring transactions and spending.

User discovery answers: first version supports **text PDFs and CSV/XLSX**; scanned statements are deferred. Audience: **personal bank and credit-card accounts**. Keep currencies separate.

User expansion: save reusable data across sessions; accept statement top-ups each month; generate updated reports understandable to an ordinary person across **savings, transaction and credit-card accounts**. Monthly refresh is invoked when files are supplied; unattended schedules/notifications have not been requested.

Latest clarification supersedes any monthly-statement assumption: statements may have arbitrary or changing frequency, including custom/ad hoc exports. Coverage is based on date ranges per account, never document counts. Monthly reporting remains a possible review cadence, not an input requirement. User proposes a distributed `banker` subagent that invokes ingestion and separate Python-backed analysis/report skills, requests missing date ranges, and synthesises findings into suggested actions and an executive summary.

User now confirms: **analyse available data immediately and label gaps**, maintaining a persistent inventory for every account and date range. Completeness is not a prerequisite for analysis. User also requests projected balances and negative-balance warnings using balances and historic mortgage, bill and subscription payments.

User further confirms: accept **multiple files at once**; Banker runs in its **own working context**, returning only summary reports and an executive summary to the main chat; use an **adjustable 30-day forecast outlook**. Context isolation is intended behaviour to verify later, not a demonstrated runtime or privacy guarantee.

Latest decisions: selected output is **executive summary plus detailed report**, without a required Excel workbook. Require a **user-set safety buffer per funding account**. Split extras into separate backlog items. Add a dedicated transaction-tagging skill using privacy-minimised vendor web lookup. Consolidate across accounts/cards, including multiple cards on one credit account and internal transfers. Storage may use files or a database, with vectors considered separately; no option selected.

2026-10-25 clarification: unsuccessful/ambiguous vendor lookup must ask the user to classify the affected transactions and retain reusable classifications for future tagging. User proposes shared transactions/accounts/tagging tables used by reporting scripts. These record groups are the starting point for storage brainstorming; database engine, detailed schema, original-file retention and deployment remain unselected.

Latest scope refinements below govern where older revision paragraphs conflict. Proposed packaging is Banker plus ingestion/coverage, tagging, and analysis/reporting skills with Python helpers; capability IDs do not imply one skill per item.

These are distributed skills, not a banking service. Reuse existing PDF and spreadsheet skills for extraction and reporting. Source files rather than bank connections are the proposed input mechanism. Analysis skills share the ingestion result to avoid repeated extraction and inconsistent totals.

Across all analyses retain account context and separate currencies: duplicate comparisons use account/currency context, unusual-transaction baselines use relevant personal-account history within each currency, and recurring groups retain account context. Consolidated spending explicitly handles transfers and repayments.

## Ranked proposal

| ID | Rank | Title | Scope revision | Status | Stage | Dependencies |
|---|---|---|---|---|---|---|
| BL-001 | 1 | Persistent ingestion, account/card inventory and coverage | 7 | Proposed | discovery | None |
| BL-009 | 2 | Transaction tagging and merchant identification skill | 2 | Proposed | discovery | BL-001 |
| BL-010 | 3 | Consolidated account/card analysis and transfer matching | 1 | Proposed | discovery | BL-001 |
| BL-002 | 4 | Duplicate transaction review | 3 | Proposed | discovery | BL-001, BL-010 |
| BL-003 | 5 | Unusual transaction review | 2 | Proposed | discovery | BL-001 |
| BL-004 | 6 | Recurring transaction analysis | 3 | Proposed | discovery | BL-001 |
| BL-005 | 7 | Spending and cash-flow analysis | 3 | Proposed | discovery | BL-001, BL-009, BL-010 |
| BL-008 | 8 | Cash-balance forecasting and shortfall warnings | 3 | Proposed | discovery | BL-001, BL-004, BL-010 |
| BL-006 | 9 | Personal finance analysis and detailed reporting | 3 | Proposed | discovery | BL-002, BL-003, BL-004, BL-005, BL-008 |
| BL-007 | 10 | Banker subagent and executive review | 4 | Proposed | discovery | BL-001, BL-006 |
| BL-011 | 11 | Fee and interest analysis | 1 | Proposed | discovery | BL-001, BL-009, BL-010 |
| BL-012 | 12 | Recurring price-change analysis | 1 | Proposed | discovery | BL-004 |
| BL-013 | 13 | Savings-goal tracking | 1 | Proposed | discovery | BL-001, BL-010 |
| BL-014 | 14 | Personal spending-budget comparison | 1 | Proposed | discovery | BL-005 |

Ranks are explicitly proposed changes from revision 5 to put prerequisites first. No active work or approved ranks existed. BL-011–BL-014 are independently selectable extras, not prerequisites for baseline reports; reports can incorporate their results when enabled. Dependencies identify capabilities to deliver, not a reason to withhold available-data analysis when some transactions lack tags or evidence. BL-003 may consume BL-009 enrichment when available without requiring resolved merchant identities for every finding.

### BL-001 — Persistent ingestion, account/card inventory and coverage

- Problem: PDF tables and bank exports vary; unverified extraction undermines all analysis.
- Intended outcome/scope: one reusable ingestion skill using existing `pdf`/`xlsx` capabilities for supplied text PDFs and CSV/XLSX from personal bank and credit-card accounts. Preserve source/page/row, raw description, account alias, dates, signed amount and currency, distinguishing unknown values. Flag extraction uncertainty, overlapping periods and reconciliation differences; identify unavailable balances rather than claiming reconciliation. Recognise scanned inputs as unsupported in this version. Keep currencies separate.
- Scope revision 2 extension: persist reusable transaction history across sessions for savings, transaction and credit-card accounts; incrementally add monthly statements. Track imports, account identity/type, source evidence and period coverage. Repeat uploads and overlapping statements must not inflate history. Explain replacement/corrected statements and user corrections without losing lineage; mark incomplete or failed imports rather than silently treating them as complete. Include user-controlled export/deletion and recoverability expectations in later requirements; persistence location and original-file retention remain open. E4 informs retention considerations. No storage engine selected.
- Scope revision 3 supersedes monthly-input wording: accept any statement frequency and changes per account, including custom/ad hoc ranges. Track the union of verified coverage intervals separately from transaction dates. Overlaps add no extra coverage; uncertain or partial imports do not silently establish complete coverage. Infer and adapt cadence per account where evidence permits, but use it only for expectations, never as proof of coverage. Assess exact gaps within an agreed review horizon and account active dates; request the missing date range, not a particular count of files. Declared statement/export range or user confirmation supports boundaries; transaction min/max alone does not. Record covered, missing, partial/failed, uncertain and unavailable ranges distinctly. A confirmed no-activity period is not equivalent to an uploaded statement. The latest covered date is not necessarily today.
- Scope revision 4 confirms a durable inventory for each account and its date ranges, updated after each import/correction. Track coverage status and supporting sources; derive exact missing intervals within the review horizon. Expose this inventory to Banker and all analyses. User reference: immediate-analysis/account-inventory clarification, 2026-10-24.
- Scope revision 5: accept multiple files in one batch, across accounts and overlapping/different periods. Record each file's outcome: imported, already represented, partially imported, failed or unsupported, with reasons/source evidence. Successful files contribute to saved history/coverage even when others fail; failed or uncertain portions do not establish verified coverage. Immediately analyse usable data, label gaps and request only unresolved ranges. Reference: user batch-upload clarification, 2026-10-24; [batch/context discovery plan](iterations/banker-batch-context-discovery-product-owner-plan.md).
- Scope revision 6: distinguish accounts from linked cards/payment instruments. Preserve account balances, debt and coverage once even when several cards share the account. Link cards using statement evidence or user confirmation; matching masked digits alone does not establish identity. Keep original-file retention, persistence location and files/database choice open for later evaluation. Evaluate exact totals, correction integrity, import recovery, portability and retention; vectors are optional similarity retrieval and must not be the source for balances or coverage. Reference: latest user storage/consolidation decisions, 2026-10-24, and [tagging discovery plan](iterations/banker-tagging-discovery-product-owner-plan.md); E11/E12/E13.
- Scope revision 7: one shared authoritative history for ingestion, tagging and reporting scripts. Consider transactions/accounts/tagging mappings as core record groups, with linked cards, dated balance observations, import/source evidence and disjoint coverage intervals as supporting records. Preserve original descriptions and transaction/posting dates where supplied. Balance observations carry date, type and source; targets and required safety buffers remain distinct user settings. Maintain correction provenance and exact monetary values with explicit currency precision rather than binary floating-point totals. Files/SQLite/service database and optional vector retrieval remain candidates, not selected schema/architecture. Reference: user storage brainstorming, 2026-10-25, [storage discovery plan](iterations/banker-storage-discovery-product-owner-plan.md), E16–E19.
- Rationale/evidence: local PDF and XLSX skills already cover extraction/import; E1 and E3 support traceability and minimisation. Shared ingestion prevents divergent analysis totals.
- Open questions: representative banks/countries/layouts; storage approach/location and original retention. Report output selected in BL-006. No samples supplied.
- Dependencies: none. Direct-request reference: user `/backlog`, 2026-10-24, and format/account discovery answers. Scope approval: pending.
- Lifecycle records: [Product Owner plan](iterations/bank-statement-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

### BL-002 — Duplicate transaction review

- Problem: repeat imports, overlapping statements and legitimately similar purchases can resemble duplicate charging.
- Intended outcome/scope: candidate groups with reasons and source evidence; distinguish repeat imports from possible repeated charges. Account for same-value purchases, refunds/reversals and pending/posted transitions where present. Preserve original records and uncertainty; do not silently delete or declare charges erroneous.
- Scope revision 2 extension: retain findings and user review decisions across monthly updates. New or corrected evidence may reopen a finding with an explanation; keep account/currency context and originals.
- Scope revision 3: consume BL-010 account/card and consolidation distinctions to avoid mistaking multiple representations of one account's activity for repeated charges. BL-010 owns transfer/economic classification; this item owns repeated-charge review. Dependencies updated in current table.
- Rationale/evidence: E2 documents duplicate-data causes and transaction-state changes. Inference: amount/date matches alone cannot prove duplicate charges.
- Open questions: representative ambiguous examples during later requirements; output now selected in BL-006.
- Dependencies: BL-001, BL-010. Direct-request reference: user `/backlog` and later consolidation request, 2026-10-24. Scope approval: pending.
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
- Scope revision 3 supersedes dedicated price-change ownership: own recurring detection, cadence and expected-payment signals, refreshed on new data regardless of statement frequency. BL-012 separately owns recurring price-change/annualised analysis. This avoids duplicate backlog scope.
- Rationale/evidence: E1 recommends accounting for periodic bills and reviewing unused subscriptions. No automatic cancellation or payment action proposed.
- Open questions: representative variable/cadence cases during requirements. Forecast need and report preference confirmed.
- Dependencies: BL-001. Direct-request reference: user `/backlog`, 2026-10-24. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-005 — Spending and cash-flow analysis

- Problem: transfers, refunds and credit-card repayments can distort spending totals across accounts.
- Intended outcome/scope: spending by category, merchant and period, with editable categorisation and traceable totals. Separate income, transfers, credit-card repayments, refunds and spending; expose uncertain matching. Report incomplete periods and uncategorised transactions. Keep currencies separate, without exchange-rate conversion.
- Scope revision 2 extension: update monthly and comparable historical summaries; retain category corrections. Include fee/interest totals and changes where identifiable (E5). Report unmatched transfers and coverage gaps; compare like periods or disclose differences.
- Scope revision 3: consume BL-009 tags and BL-010 consolidation/transfer classifications for core spending/cash-flow summaries. Dedicated fee/interest analysis belongs to BL-011, budget comparison to BL-014; underlying transactions remain in complete totals. Transfers/repayments affect account cash flow without duplicating household spending. Unresolved tags or transfer candidates remain visible rather than blocking the report.
- Rationale/evidence: E1 supports categorising spending. Cross-account double-counting controls are a proposed product requirement, not an existing demonstrated capability.
- Open questions: category preferences during requirements. Report output selected in BL-006.
- Dependencies: BL-001, BL-009, BL-010. Direct-request reference: user `/backlog`, 2026-10-24, personal-account/currency answer and latest tagging/consolidation decisions. Scope approval: pending.
- Lifecycle records: shared discovery plans linked under BL-001. Completion evidence: none.

### BL-006 — Personal finance analysis and detailed reporting

- Problem: monthly top-ups need one understandable review of changes across accounts rather than disconnected analyses or repeatedly rebuilt history.
- Intended outcome/scope revision 1: one skill orchestrates the preceding skills when statements are added, then saves a refreshed plain-language report and report history. Explain where money went, what changed and what needs review. Include covered accounts/periods, balance as-of dates, missing inputs, source evidence and material corrections; distinguish revised reports from earlier versions. Show deposit-balance and credit-card debt trends when supported. Report format remains open; an Excel companion is proposed, not confirmed.
- Scope revision 2 supersedes the earlier orchestration boundary: a separate analysis/report skill uses accompanying Python scripts for repeatable calculations and traceable findings across BL-002–BL-005, then produces detailed reports and saved report versions. Reuse existing document skills as appropriate. Reports may cover a chosen month or other horizon regardless of input statement frequency; identify coverage limitations and qualify affected comparisons. Banker (BL-007) owns conversational coordination and executive synthesis. Proposed grouping is two skills plus Banker; backlog capabilities need not map one-to-one to skills. No script interface or storage architecture selected.
- Scope revision 3: produce the selected detailed report with consolidated household/account/card views and drilldowns supported by evidence; Banker supplies the executive summary. Python performs repeatable calculations; reuse document skills for presentation. Excel is an optional future review/export format, not required output or the chosen storage method. Consume BL-008 forecast results and enabled BL-011–BL-014 extras without making extras report prerequisites. Tagging is now a separate skill (BL-009), superseding the two-skill grouping.
- Scope split: BL-011 fee/interest, BL-012 recurring price changes, BL-013 savings goals and BL-014 budgets are separately selectable. Report may show statement-supplied card due dates/minimum payments and BL-008 upcoming-bill projections, never guaranteeing affordability/current funds.
- Rationale/evidence: user explicitly requested monthly top-ups and updated ordinary-person reports. E1/E5–E7 support the proposed review menu; stored report lineage supports explainability after corrections.
- Open questions: final detailed-report file format; individually selected extras; history location and original retention. Executive summary plus detailed report is confirmed.
- Dependencies: BL-002, BL-003, BL-004, BL-005, BL-008. Direct-request reference: user persistence/report expansion and latest report/consolidation decisions, 2026-10-24. Scope approval: pending.
- Lifecycle records: [Monthly Product Owner plan](iterations/bank-statement-monthly-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

For BL-001–BL-005, scope revision 2 additionally references the user monthly persistence/report expansion on 2026-10-24 and the monthly Product Owner plan above. Original request references remain intact. No prior scopes were approved.

### BL-007 — Banker subagent and executive review

- Problem: users need one conversational guide to gather missing inputs, invoke repeatable analyses and explain what matters across accounts.
- Intended outcome/scope revision 1: add a distributed subagent named `banker`; it invokes ingestion/coverage and analysis/reporting skills, presents missing or uncertain date ranges, requests inputs that cover those ranges, and remembers supplied coverage. Adapt to each account's observed statement timing without requiring fixed periods or counts. Turn calculated summaries from one or more skills into a plain-language executive summary and prioritised suggested actions, with numerical claims traceable to results and source evidence.
- Scope revision 2: user confirms immediate available-data analysis with gaps labelled, rather than waiting for completeness or asking permission to proceed. Consult/update the durable account/date-range inventory; ask for missing ranges alongside results and refresh affected findings after new data arrives. Label affected comparisons and forecasts provisional or unavailable where evidence is insufficient; never invent missing transactions/balances. Present BL-008 shortfall warnings prominently when forecast results are available. User reference: immediate-analysis/account-inventory clarification and forecast request, 2026-10-24.
- Scope revision 3: Banker works in its own isolated working context. The main chat receives summary reports and the executive summary, including material warnings, data limitations and unresolved missing-range requests. Detailed transaction records, extraction outputs and processing logs remain in Banker's context or saved artifacts. Resume from durable inventory, history, corrections, findings and report records rather than previous chat context. Numeric claims remain traceable to saved results. Actual isolation/handoff must be verified later; this is not a demonstrated privacy boundary. Reference: user context-separation clarification, 2026-10-24; batch/context discovery plan linked under BL-001.
- Scope revision 4: invoke the dedicated tagging skill where needed, surface ambiguous tags/consolidation and missing buffer settings without withholding other findings. Executive synthesis covers supplied accounts collectively with account-specific risks and evidence-supported card breakdowns. Selected summary+detailed report output supersedes workbook-related uncertainty. Reference: latest user tagging/report/consolidation decisions, 2026-10-24; tagging discovery plan under BL-001.
- Boundaries: separate facts, uncertain interpretations and optional actions. Suggested checks may concern an unfamiliar charge, recurring price change or missing data. Sending messages, disputing charges, cancelling services and moving money remain outside scope. No autonomous financial actions or schedules proposed.
- Rationale/evidence: direct user Banker brainstorming and variable-frequency/range-coverage clarification, 2026-10-24. Existing agent definitions and skill Python helpers establish repository conventions, not implemented financial capability.
- Dependencies: BL-001, BL-006. Open questions: review-horizon onboarding, summary format, storage/retention. Tagging adds a third skill responsibility; immediate analysis, inventory, own context and summary+detailed output are confirmed. Status Proposed; stage discovery; approval pending.
- Lifecycle records: [Banker Product Owner plan](iterations/banker-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

BL-001 scope revision 3 and BL-006 scope revision 2 additionally reference the Banker brainstorming and coverage clarification, 2026-10-24. All earlier approved scope remains absent; previous drafts are preserved rather than treated as approval.

### BL-008 — Cash-balance forecasting and shortfall warnings

- Problem: historic reports do not show whether payment timing could cause an upcoming shortfall in the account funding a payment.
- Intended outcome/scope revision 1: Python-backed analysis projects cash balances per funding account over an adjustable horizon, using a dated balance and expected income, mortgage payments, bills, subscriptions, card repayments, transfers and any explicit ordinary-spending allowance. Use history-based estimates and user-confirmed commitments with labelled dates, amounts and assumptions. Show first projected negative date, lowest projected balance, contributing payments and uncertainty; positive funds elsewhere must not hide an account-specific shortfall.
- Scope revision 2: default to a user-adjustable 30-day outlook. Show forecast start/end dates and starting balance as-of date; an older statement balance is not made current by this horizon. Reference: user horizon confirmation, 2026-10-24; batch/context discovery plan linked under BL-001.
- Scope revision 3: require a user-set safety buffer per funding account in its currency. Report below-buffer and below-zero crossings separately. Never invent a threshold. If absent, request the buffer and mark buffer assessment unavailable while continuing negative-balance analysis. Consume BL-010 transfer/account distinctions. Reference: user's option 3C and consolidation decision, 2026-10-24; tagging discovery plan under BL-001.
- Balance semantics: identify whether the starting value is statement closing, current/ledger or available balance and its as-of date. Request a fresher balance if needed; old closing balances are not current funds. Avoid counting pending payments already reflected in the starting balance, or show scenarios when uncertain. Reconcile overlapping recurring/mortgage/bill candidates so one obligation appears once. Card purchases affect debt; bank repayments affect cash. Internal transfers/card repayments are cash movements without being additional consolidated spending.
- Forecast scenarios: baseline and cautious scenarios may vary income/payment timing or variable bills. Unknown same-day posting order cannot establish precise intraday safety. Carry missing-range/account warnings, limited history, unseen commitments and stale balances into the result. Immediate analysis remains the default; if no defensible starting balance exists, return the available descriptive analysis and state that a numeric balance projection is unavailable pending input. A positive projected balance means no shortfall under stated assumptions, not guaranteed safety.
- Warning output: a prominent account-specific warning during a user-invoked review or data refresh, with drivers and suggested checks. BL-006 includes detailed forecast results; BL-007 synthesises warnings/actions. No background monitoring, scheduled notifications or automatic transfers/payment changes are included.
- Rationale/evidence: direct user forecast/alarm request, 2026-10-24; E8 supports timed cash-flow projections, E9 supports timing-shortfall context and E10 informs balance distinctions. Proposed capability within the analysis skill, not necessarily another skill.
- Dependencies: BL-001, BL-004, BL-010. Open inputs: actual per-account buffers and commitments during use. Required buffers and adjustable 30-day default are confirmed. Scope approval pending; status Proposed; stage discovery.
- Lifecycle records: [Forecast Product Owner plan](iterations/balance-forecast-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

## New individually tracked capabilities

BL-009 scope revision 2; BL-010–BL-014 scope revision 1. All: status Proposed; stage discovery; approval pending; completion evidence none. Direct reference: user tagging/consolidation and split-extra decisions, 2026-10-24; BL-009 additionally references user fallback/mapping clarification, 2026-10-25. Lifecycle records: [tagging Product Owner plan](iterations/banker-tagging-discovery-product-owner-plan.md), [storage Product Owner plan](iterations/banker-storage-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Ranks/dependencies are in the current table; no scope is automatically approved.

### BL-009 — Transaction tagging and merchant identification skill

- Problem: transaction descriptions can obscure vendors and spending types.
- Outcome/scope: a separate skill assigns reviewable merchant identities, categories and user tags, reusing confirmed mappings before web lookup. Locally derive the smallest safe business-name query; broad business context only if needed. Never blindly transmit full descriptions, amounts, transaction dates, account/card identifiers, personal names or reference numbers. If a safe business-only query cannot be formed, leave unresolved or ask the user. Prefer the merchant's public site and record source URL, lookup date, rationale and uncertainty. A business identity does not prove the specific goods/services purchased. User corrections persist and take precedence over inference, with history. Treat web content as evidence, not instructions. No enrichment API selected.
- Scope revision 2: if lookup fails or remains ambiguous, ask the user to classify the affected transactions, while other analysis continues. Save the answer and its provenance; distinguish this-transaction-only corrections from reusable future-matching rules. Offer and record the chosen matching scope rather than silently applying one purchase's category to every transaction from that vendor. Transaction-specific corrections override reusable suggestions. Unanswered items stay visibly unresolved; confirmed reusable rules are checked before future web lookup. All scripts use the same saved classifications/history.
- Evidence/rationale: direct request; E14 shows merchant/category enrichment as distinct evidence with confidence; E15 informs minimisation. Merchant-only queries reduce disclosure but do not guarantee anonymity.
- Open questions: category taxonomy, review threshold and handling business names that may identify individuals during requirements. Do not require resolved tags for all transactions before analysis.

### BL-010 — Consolidated account/card analysis and transfer matching

- Problem: several accounts/cards and two sides of a transfer can inflate spending, balances or liabilities.
- Outcome/scope: consolidate supplied accounts within each currency, retaining account views. Several cards can be instruments on one credit account; count debt/balance/coverage once and offer per-card breakdown only when evidence supports it. Match transfers and card repayments using traceable candidate links; retain unmatched or ambiguous cases and do not match solely on equal amounts. Distinguish refunds/reversals from income and link to spending where identifiable. No silent merging or deletion of original transactions.
- Ownership: consolidated economic classification here; duplicate-charge review in BL-002; spending in BL-005; future cash movement in BL-008. Transfers and card repayments affect account cash flow but not household spending twice.
- Evidence/rationale: direct user consolidation request; E13 illustrates linked additional cards, E2 informs ambiguous representations.
- Open questions: account ownership/linkage and cross-account examples during requirements; partial coverage can leave one transfer side unmatched.

### BL-011 — Fee and interest analysis

- Problem/outcome: separately explain identifiable bank/card fees, interest charged/earned and changes, with source evidence and uncertain classifications. No inferred effective rates without adequate balances/terms. Underlying rows remain in core financial totals; this item owns the dedicated analysis.
- Evidence/rationale: user asks extras split; E5/E7 support review of interest/fees.
- Open questions: which fee/interest groupings to emphasise; optional feature selection.

### BL-012 — Recurring price-change analysis

- Problem/outcome: compare like recurring payments and explain changed amounts, with annualised scenarios only when assumptions are explicit. Variable usage or changed frequency is not automatically a price rise. BL-004 owns recurrence detection; this item owns comparative price-change interpretation.
- Evidence/rationale: user asks extras split; E1 supports recurring-cost review.
- Open questions: sufficient evidence for a like-for-like price comparison; optional feature selection.

### BL-013 — Savings-goal tracking

- Problem/outcome: compare user-entered targets/dates with selected account balances, distinguishing deposits/transfers, interest and balance growth. Moving money between owned accounts does not create external income or household savings. No invented targets.
- Evidence/rationale: user asks extras split; E6 supports savings goals/progress.
- Open questions: target, selected accounts and dates provided during use; optional feature selection.

### BL-014 — Personal spending-budget comparison

- Problem/outcome: compare user-set category/period budgets with classified spending, showing uncategorised activity and incomplete coverage. Do not invent personal budgets. Keep budgets distinct from mortgage/bill commitments and account safety buffers.
- Evidence/rationale: separately tracked option requested by user; product inference extending E1 spending categories, not a demonstrated accuracy claim.
- Open questions: category/period budget inputs and optional feature selection.

## Storage and workbook distinction

Storage remains open: evaluate authoritative structured history in files or a database for exact calculations, stable identity, corrections, recovery and portability; retain source/report files according to chosen retention policy. Optional vector retrieval may help find similar descriptions/explanations, but must not determine balances, coverage or exact transaction identity from approximate matches. E11 and E12 support these different purposes, not a choice of technology. No database, vector service or embedding transfer approved.

### Storage brainstorming — 2026-10-25

| Candidate | Product fit / tradeoff |
|---|---|
| CSV/JSON files | Easy inspection/export; linked corrections, import outcomes and consistent updates require additional care |
| SQLite | Strong candidate for individual local use: shared structured records in a database file, accessible through Python without a separate server; not selected |
| Service database | Candidate when multiple users/devices/sessions must update shared history concurrently; additional operational decisions |
| Optional vectors | Similar-description/explanation retrieval only; defer unless a demonstrated use case justifies it |

Core conceptual records, not an approved schema:

- Transactions across all accounts/cards: stable identity, account/card links, signed exact amount/currency, transaction/posting dates, raw description, merchant/tags and source/correction references.
- Accounts: bank/type/currency, active dates, linked instruments, user target and required safety buffer. A latest balance may be a convenient view of dated observations, never an undated assertion of live funds.
- Tagging mappings: confirmed match criteria, assigned merchant/category/tags, reusable scope, provenance and corrections. Transaction-only overrides must not become blanket vendor rules.
- Supporting records: linked cards; dated balance observations; import/file outcomes and transaction-to-source evidence; coverage intervals. One minimum/maximum date cannot represent a gapped history, and one transaction can appear in multiple overlapping imports.

Reporting scripts read the same authoritative data and saved tags; they must not create competing versions of history. Exact amount representation must respect currency precision (for example suitable minor units or decimal arithmetic), not assumed two-decimal binary floats. E16–E19 inform this discussion; no database/schema/interface selected, scripts run or storage trial performed.

The proposed workbook was for filtering transactions, inspecting/correcting tags, checking totals and export. It is not required by the selected executive-summary/detailed-report output and does not decide persistence. It is excluded as a required deliverable.

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
- **E11 — Integrity example:** [PostgreSQL transactions](https://www.postgresql.org/docs/16/tutorial-transactions.html). Illustrates atomic updates; not a selected database.
- **E12 — Retrieval example:** [OpenSearch vector-search basics](https://docs.opensearch.org/latest/vector-search/getting-started/vector-search-basics/). Describes similarity retrieval; optional role differs from authoritative exact financial calculations.
- **E13 — Additional cards:** [CommBank additional-cardholder guidance](https://www.commbank.com.au/support.credit-cards.add-additional-cardholder.html). Illustrates an additional card on an account; bank-specific example, not a universal statement-layout assumption.
- **E14 — Enrichment:** [Plaid enrichment documentation](https://plaid.com/docs/api/products/enrich/). Distinguishes merchant/category enrichment and confidence; no API integration or lookup accuracy claimed.
- **E15 — Minimisation:** [OAIC APP 3 guidance](https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-3-app-3-collection-of-solicited-personal-information). Informs data minimisation; legal applicability unassessed and queries are not guaranteed anonymous.
- **E16 — SQLite fit:** [SQLite appropriate uses](https://www.sqlite.org/whentouse.html). Informs local application storage versus client/server concurrency tradeoffs; not a selected engine.
- **E17 — Python access:** [Python sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html). SQLite can be accessed without a separate server process.
- **E18 — Numeric accuracy:** [SQLite floating-point documentation](https://www.sqlite.org/floatingpoint.html). Explains binary floating-point approximation.
- **E19 — Decimal arithmetic:** [Python decimal documentation](https://docs.python.org/3/library/decimal.html). Supports discussion of exact decimal arithmetic/accounting requirements; implementation representation unselected.

Research performed by Product Owner on 2026-10-24 using generic public queries. Limitations: public documentation only, no private data submitted, no bank samples supplied, no representative-layout testing, no measured extraction/detection accuracy, no legal assessment. User preferences beyond the recorded discovery answers remain unconfirmed.

DISC-BANK-002 expanded public-source research on the same date. No persistence/recovery trials or report-generation tests performed; evidence supports proposed user needs, not demonstrated functionality.

DISC-BANK-004 researched E8–E10 using generic public queries on 2026-10-24. No private data, forecast tests or accuracy evidence; jurisdiction-specific banking rules not assessed.

DISC-BANK-007 researched E11–E15 using generic public queries on 2026-10-24. No private transactions submitted; no tagging, storage, embeddings or consolidation trials performed. Sources inform distinctions and product needs, not a tested implementation or selected architecture.

DISC-BANK-008 researched E16–E19 on 2026-10-25 using generic public queries. No private transactions, database creation, schema selection, scripts or storage tests. Recommendation is to evaluate SQLite as a strong candidate, not a demonstrated or selected implementation.

## Remaining discovery questions

1. Later evaluation: authoritative storage approach/location, source retention, export/deletion/recovery; whether optional vector retrieval has a demonstrated need. No choice required for discovery approval.
2. Which exact detailed-report format and representative banks/countries/layouts should requirements target? No bank examples supplied.
3. Which individually tracked extras BL-011–BL-014 should become Ready with the core items? Scope split does not automatically prioritise delivery.
4. Later requirements: tagging taxonomy/review thresholds, account/card linkage evidence and transfer ambiguity examples; later use: actual buffers, savings targets and budgets.
5. Storage evaluation: one local user/session at a time or several devices/sessions updating shared history? Retain source statements alongside history or references only with originals managed separately? These remain open choices, not approval prerequisites for discovery.

Resolved: immediate analysis/gap labels; persistent account/range inventory; batch uploads; Banker own context/main-chat summaries; adjustable 30-day forecast; required user-set per-account buffers; summary+detailed report, no required workbook; separate tagging skill; consolidated accounts/cards/transfers; extras separately tracked. Do not re-ask these decisions.

## Revision and decision history

Discovery choice round DISC-BANK-006 r1 (2026-10-24; historical options, superseded by user answers recorded below):

| Decision | A (recommended) | B | C |
|---|---|---|---|
| Persistence | Chosen folder with copies of statements, history and reports | Chosen folder with history/reports only; originals managed separately | Existing personal data store specified by user |
| Deliverables | Executive summary, detailed report and Excel workbook | Executive summary and detailed report | Executive summary and Excel workbook |
| Warning threshold | Below zero plus optional per-account buffer | Below zero only | Required user-set per-account buffer |
| First-version extras | Core analyses/forecast, fees, interest and recurring price changes | Core plus savings goals | Core plus savings goals and user-set spending budgets |

User answers: persistence unresolved (files/database/vectors to evaluate); deliverables B (summary+detailed report, workbook purpose questioned); warning C (required per-account user buffer); extras split into separate items. Earlier recommendations are not approvals. Distinguish insufficient evidence to forecast from no projected shortfall prominently. [Final discovery plan](iterations/banker-final-discovery-product-owner-plan.md); latest reconciliation in tagging discovery plan under BL-001.

- 2026-10-24 — Revision 1 draft: Coordinator created backlog from Product Owner DISC-BANK-001 r1 discovery. No existing backlog found; existing workflow iteration record preserved. IDs BL-001–BL-005 allocated once; earlier BL-style task IDs in that iteration record are assignment tasks, not feature IDs.
- 2026-10-24 — User confirmed text PDFs/CSV/XLSX first, scans later; personal bank/credit-card accounts; separate currencies. Incorporated before revision 1 approval proposal. No rank change.
- 2026-10-24 — Product Owner refinement DISC-BANK-001 r2 reconciled all five scopes with these answers; persisted in revision 1 draft before presentation.
- 2026-10-24 — Revision 2 draft: user expanded scope to durable history, monthly top-ups and refreshed personal reporting across savings, transaction and card accounts. Product Owner DISC-BANK-002 r1 refined BL-001–BL-005 to scope revision 2; Coordinator allocated BL-006 scope revision 1 at rank 6. Earlier ranks retained; exact unapproved revision 1 archived. No active work or approval invalidated because none existed.
- 2026-10-24 — Revision 3 working draft: user proposed Banker, separate Python-backed analysis/reporting and executive synthesis, then clarified arbitrary/changing statement frequency with date-range coverage as the criterion. Product Owner DISC-BANK-003 r1 refined boundaries and interval semantics. Coordinator retained existing IDs/ranks and allocated BL-007 at rank 7; BL-001 advanced to scope revision 3 and BL-006 to scope revision 2. Exact r2 draft archived. No code or skills implemented.
- 2026-10-24 — Revision 4 working draft: user requested projected balances/negative-balance alarm and confirmed immediate analysis with durable per-account/range inventory. Product Owner DISC-BANK-004 r1 researched/proposed forecast capability; Coordinator allocated BL-008 scope revision 1 at rank 8 and incorporated explicit immediate-analysis decision in BL-001 r4 and BL-007 r2. Original ranks retained; exact r3 snapshot preserved. No forecasts run or monitoring created.
- 2026-10-24 — Revision 5 working draft: user confirmed multi-file uploads, separate Banker working context with summary-only main-chat handoff, and adjustable 30-day forecast default. Product Owner DISC-BANK-005 r1 reconciled direct decisions; Coordinator saved BL-001 r5, BL-007 r3, BL-008 r2 and exact r4 snapshot. IDs/ranks unchanged; safety-buffer preference remains open. No implementation or runtime verification performed.
- 2026-10-24 — Revision 6 proposal: user clarified storage uncertainty, output B, warning C, separate extras, merchant tagging and consolidated multiple-account/card reporting. Product Owner DISC-BANK-007 r1 researched E11–E15 and proposed dependency-first ranks. Coordinator allocated BL-009–BL-014 once, advanced scopes per current table, narrowed older ownership to avoid duplicate tagging/consolidation/extra analyses, and preserved exact r5 snapshot. Rank changes explicitly proposed, not approved; no active work existed. No implementation performed.
- 2026-10-25 — Revision 7 working draft: user requested mandatory user classification after unsuccessful vendor lookup and brainstorming shared transaction/account/tagging records for scripts. Product Owner DISC-BANK-008 r1 researched E16–E19 and refined BL-001 r7/BL-009 r2; Coordinator preserved r6 snapshot and existing IDs/ranks. Supporting record responsibilities discussed, no schema or engine selected. No implementation performed.
- Approval pending: revision 6 approval proposal superseded by continued storage brainstorming in revision 7. No approval demand during this brainstorm. Later explicit approval must identify exact revision/subset; only identified scopes become Ready. Storage evaluation and downstream approvals remain separate. No feature completion claimed.
