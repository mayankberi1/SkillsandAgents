# BL-001 ingestion requirements — revision 3

Date: 2026-10-26. Assignment: PLAN-BANK-001 r3. Backlog: revision 8, BL-001 scope revision 8, approved under APR-BANK-008. Stage: requirements. **Approved under APR-ING-REQ-003**, user message “approved”, 2026-10-26. Approval covers requirements revision 3, ING-001–ING-014, header-period acceptance cases, ING-010-A–J and explicit defaults. Architecture, solution design, iteration and implementation approvals remain separate.

## Outcome and boundary

A person can supply one or more personal bank or credit-card statements, retain original copies and reusable history locally, and receive an accurate account/date-range inventory showing imported information, uncertainty and missing inputs. Later skills reuse that same history.

Deliver a distributed ingestion/coverage skill using existing document extraction capabilities and appropriate Python helpers. This repository is a distribution collection; this feature does not create a banking service.

In scope: savings, transaction and credit-card accounts; generic text PDFs and CSV/XLSX; SQLite persistence; retained originals; accounts/cards, exact amounts, dated balances, import provenance, corrections, reimports, coverage and ingestion outcomes.

Out of scope: OCR/scanned-statement extraction, bank connections, merchant lookup/tagging execution, transfer classification, suspected duplicate-charge detection, spending/forecast/report calculations, Banker implementation, workbook generation, scheduled work, service databases and embeddings. Import deduplication belongs here; deciding whether a bank charged twice belongs to BL-002. Preserve later skills' settings and review decisions without implementing their behaviour.

## Requirements and acceptance criteria

All requirements below are Must unless explicitly identified as proposed operational defaults.

### ING-001 — Supported inputs and extraction reuse

Accept individually supplied files or batches of text PDFs, CSV and XLSX without requiring a named-bank parser. Reuse existing PDF/spreadsheet extraction capabilities; add banking interpretation rather than replacement general document tooling.

- **Positive:** representative text PDF, CSV and XLSX fixtures produce identifiable transaction observations and source locations.
- **Negative:** image-only PDFs, unreadable/corrupt files and unsupported layouts receive explicit unsupported/failed/partial outcomes; no OCR or invented rows.
- Generic support means evidence-based interpretation, not universal bank-format compatibility.
- Read supplied files without modifying them. Extracting XLSX data does not require delivering a workbook or recalculating/saving the input.

### ING-002 — One local dataset and retained originals

Use one user-designated local personal SQLite dataset with original copies in an associated source folder. Shared history is authoritative for later ingestion, tagging, analysis and reporting capabilities.

- **Positive:** after a completed import and a new session, the same dataset exposes prior transactions, account inventory, coverage, sources and corrections without chat reconstruction.
- **Negative:** a new session must not silently create a different empty dataset when the configured one is unavailable.
- Copies preserve source content. Same-named different files must not overwrite each other; repeated sources remain rHey ecognisable.
- **Proposed default:** ask for a dataset location on first use and remember it. No assumed external/home directory or silent repository storage.
- If the database or retained copy cannot be saved, affected records must not be reported as fully persisted.

### ING-003 — Source-linked transaction observations and unknowns

Preserve source reference and page/table-row or sheet/row location, original description, account association, signed amount, currency and dates. Preserve transaction date and posting date separately when supplied.

- **Positive:** each active transaction observation can be traced to original source evidence and any subsequent correction.
- **Negative:** missing posting date, merchant or balance remains unknown; do not fabricate a date, use zero for missing money, or infer merchant identity.
- Ambiguous date formats, amount conventions, acmichaelcount association or currency remain explicitly unresolved. Request only the clarification needed for affected observations.
- Preserve trustworthy observations from otherwise partial files; unresolved financial values do not contribute to verified totals.

### ING-004 — Exact money and currency separation

Store and process monetary values exactly at explicitly known currency precision. Resolve debit/credit signs from source conventions or user clarification.

- **Positive:** exact-value fixtures retain their original amounts after import, retrieval and correction, without binary floating-point drift.
- **Negative:** different currencies must not be combined, converted or silently treated as one currency. A currency symbol alone must not resolve ambiguous currencies without other evidence.
- Excess/uncertain precision is surfaced rather than silently rounded. Representation choices belong to design.

### ING-005 — Account identity, linked cards and settings

Maintain durable account aliases, institution/type/currency where known, expected-account membership and active dates when available. Distinguish an account from its linked cards/payment instruments.

- **Positive:** two evidenced cards sharing one credit account retain their card attribution while account debt/balances and account coverage are represented once.
- **Negative:** identical masked suffixes alone cannot merge accounts/cards; uncertain associations remain unresolved.
- **Proposed default:** use source evidence for confident linkage and ask before resolving ambiguity; do not silently merge existing accounts.
- A card's limited transaction list does not establish complete account coverage.
- User targets/buffers remain distinct from observed balances. Existing settings and later-stage user decisions survive new imports; configuring their downstream behaviour is outside this feature.

### ING-006 — Dated balance observations and reconciliation

Preserve each supplied balance with account, currency, as-of date, balance type and source. Distinguish statement closing, opening, current/ledger and available balance when evidenced.

- **Positive:** multiple statement balances remain available as dated observations; any latest-balance view identifies its date and meaning.
- **Negative:** a historical closing balance is never presented as a live balance; unavailable balance fields remain unknown.
- Reconcile opening balance, supported account movements and closing balance only when the source provides a sufficient, understood basis.
- Return reconciliation outcome as matched, discrepancy or unavailable, with evidence and explanation.
- A discrepancy must not trigger manufactured adjustment transactions or silently changed source amounts.

### ING-007 — Header-based statement periods and durable coverage

Maintain per-account coverage intervals separately from observed transaction dates. Obtain statement start/end dates **only from explicit statement-period information in the document header, or from an explicit user answer**.

- Record each boundary's source: header evidence/location or user answer.
- If either boundary is missing, ambiguous or contradictory, ask the user for the unresolved boundary or corrected period. Do not invent or default dates.
- Do not derive statement periods from transaction dates, inactivity, footer/body text, filenames, file timestamps, cadence or neighbouring statements.
- For CSV/XLSX, use explicit statement-period header metadata when present. Ordinary transaction-column headings and transaction rows do not establish a statement period; otherwise ask the user.
- Preserve successfully extracted transactions immediately while coverage remains unconfirmed. Confirmed boundaries alone do not make a partial extraction complete or a card-specific subset full-account coverage.
- Union verified intervals without multiplying overlapping coverage; retain disjoint intervals. Statement frequency changes do not alter this rule.

**Acceptance cases**

| Case | Expected result |
|---|---|
| Header says 1–31 January; no transactions | A successfully processed full-account statement establishes that period; inactivity creates no gap. |
| Header says 1–31 January; transactions span 8–20 January | Coverage remains 1–31 January, not 8–20 January. |
| One header boundary is missing | Preserve the evidenced boundary; ask for the other. Do not substitute a transaction date. |
| Both header dates are missing | Ask for both; preserve extracted transactions with unconfirmed coverage. |
| Header dates are ambiguous, contradictory or reversed | Ask for clarification; do not select an interpretation silently. |
| CSV/XLSX has transactions but no statement-period header metadata | Ask for the period; transaction minima/maxima do not establish it. |
| User supplies missing/corrected boundaries | Record the answer and its provenance, then reassess coverage subject to extraction/account-scope checks. |
| Filename/footer/body/cadence suggests dates absent from the header | Those suggestions do not establish coverage. |

### ING-008 — Gaps, expected accounts and immediate availability

Calculate missing intervals within a supplied review horizon and known account active dates. Distinguish verified coverage, missing ranges, uncertain boundaries, partial/failed imports and user-declared unavailable/no-activity periods.

- **Positive:** the inventory identifies exact uncovered intervals for each expected account and explains why a range is not verified.
- **Negative:** user-confirmed no activity does not masquerade as an uploaded/verified statement; unavailable data does not become zero transactions.
- **Proposed default:** when no horizon exists, ask for it while exposing imported facts immediately. Do not silently extend the horizon to today.
- Successful usable data becomes available to later capabilities immediately despite gaps. This feature returns coverage limitations; it does not wait for completeness or execute downstream analysis.
- Requests concern unresolved date ranges, not an assumed number of monthly statements.

Distinguish an unknown statement period from a confirmed uncovered interval. Do not infer missing coverage from days without transactions. Requests for missing or ambiguous header boundaries do not block extraction or availability of usable transactions; label affected coverage and downstream conclusions unconfirmed until resolved.

### ING-009 — Batch outcomes and partial failure

Return a durable per-file outcome: imported, already represented, partially imported, failed or unsupported, with reasons and relevant counts/uncertainties.

- **Positive:** a valid file succeeds even when another batch member fails; both outcomes remain visible after restart.
- **Negative:** one failed file must not discard earlier successful imports or mark its unverified date ranges complete.
- Partially imported files identify accepted versus unresolved portions. Outcome summaries distinguish source observations from newly added active transactions.
- Repeated invocation does not hide a previous failure or claim an unperformed retry succeeded.

### ING-010 — Repeat files and overlapping transaction observations

Prevent repeated or overlapping imports from inflating active transaction history, balances or coverage. Retain each source's observations and provenance separately from their active transaction representation.

1. **Exact-file repeats:** identify repeated file contents using a content digest, not filename. A previously completed, unchanged source with no unresolved work returns “already represented” without adding transactions. A partial, failed or interrupted import must remain eligible for safe retry; file recognition alone cannot mark it complete.
2. **Cross-file overlap:** inspect incoming observations even when their date range is already covered. Match within the same established account using a trustworthy provider transaction reference when supplied and understood. Such references are not guaranteed present, permanent or globally unique; conflicts remain unresolved.
3. **Candidates without reliable references:** use conservative one-to-one comparison of available normalised evidence: transaction/posting dates with their meanings preserved, exact signed amount, currency, description and optional evidenced card attribution. These fields generate matching evidence, not a globally unique fingerprint. Filenames and row/page positions identify provenance, not cross-file transaction identity.
4. **Multiplicity:** one existing observation cannot automatically absorb several incoming rows. Preserve legitimate repeated purchases, including identical date/amount/description combinations. Where repeated observations cannot be distinguished reliably, retain uncertainty rather than silently merging or adding them as verified transactions.
5. **Outcomes:** link confidently repeated observations to the existing active transaction while retaining the new source evidence; add confidently new transactions. Preserve ambiguous candidate observations without counting them as additional verified activity; expose the affected portion and clarification needed. Never remove already verified legitimate activity merely because another source is ambiguous.
6. **Changed observations:** pending-to-posted transitions, changed amounts/descriptions and corrected/replacement statements are not automatically exact duplicates. Use supported linkage/state evidence or ING-011 correction handling; otherwise retain uncertainty. Do not classify refunds or similar opposite-sign transactions as duplicates merely because other fields match.
7. **Persistence and retry:** persist accepted transaction representations, source links and import progress consistently so an interrupted retry neither duplicates committed work nor loses unresolved work. Do not claim whole-import or filesystem atomicity merely because SQLite supports transactions. Detailed transaction boundaries belong to design.

**Acceptance criteria**

| ID | Observable case and expected result |
|---|---|
| ING-010-A | Import a completed monthly statement again, including under a different filename: no additional active transactions or multiplied coverage; report already represented. |
| ING-010-B | Import a changed file using the same filename: detect changed content, examine its observations and apply overlap/correction rules rather than skipping or overwriting it. |
| ING-010-C | Import January, then an annual statement: confidently matched January transactions gain annual-source provenance without duplicate active entries; confidently new annual transactions are added. Ambiguities remain visible. Do not skip the annual file or the whole January interval. |
| ING-010-D | Import the annual statement, then January: confidently repeated January observations gain monthly-source provenance; active transaction counts and totals remain unchanged. |
| ING-010-E | Two legitimate identical purchases occur within a statement: retain both. When another source also contains both, matching must respect multiplicity; unresolved identity must not silently reduce two purchases to one or inflate them to four verified purchases. |
| ING-010-F | A trusted provider reference identifies the same account transaction across sources: retain one active representation with both source links. The same reference appearing in another account must not merge those accounts' activity. Conflicting reference evidence is flagged. |
| ING-010-G | Only date/amount/description match, with insufficient evidence of sameness: preserve candidate uncertainty; do not automatically delete, merge or declare duplicate bank charging. |
| ING-010-H | Pending and posted versions have changed dates/amounts: apply evidenced state linkage or retain uncertainty; do not count both as verified separate completed activity solely because their values differ. |
| ING-010-I | Interrupt an import after some accepted work persists, then retry: no duplicate committed transactions/source links; remaining work is retried, and the final outcome accurately distinguishes completed and unresolved work. |
| ING-010-J | A covered period contains an incoming previously unseen transaction: investigate/add it when supported or flag the discrepancy. Coverage alone is never proof that every incoming row is already represented. |

Technical evidence for the proposed behaviour: [Python hashlib](https://docs.python.org/3/library/hashlib.html) supports source-content hashing, which cannot establish cross-file financial identity. [SQLite transactional guarantees](https://www.sqlite.org/transactional.html) support consistent database updates, not whole-filesystem/import atomicity. These references inform later design; no schema, code or tested guarantees are implied.

### ING-011 — Corrections and replacement statements

Accept user corrections and replacement/corrected sources while retaining original evidence, prior values, reason/source of change and active/superseded status.

- **Positive:** a corrected amount or account association changes the active observation and affected inventory, while prior evidence remains traceable.
- **Negative:** a similar filename or later upload alone must not supersede previous history.
- **Proposed default:** ask which source/range is replaced when intent is ambiguous. Clear user replacement instructions need not be reconfirmed.
- Preserve unrelated records and user decisions. Changed observations expose that their earlier derived results may be stale; this feature does not regenerate other features' analyses.
- Coverage must be recomputed when corrections invalidate a previously verified boundary or account association.

### ING-012 — Persistence failure, recovery and retention control

Committed history survives restart. Interrupted or failed persistence must leave an intelligible recoverable state without false success claims.

- **Positive:** reopening after an interrupted import identifies which work persisted; retry does not duplicate previously committed observations.
- **Negative:** an inaccessible, incompatible or damaged dataset must not be overwritten or silently reset.
- Provide user-controlled export/recovery and deletion behaviour for managed history and retained sources.
- **Proposed defaults:** retain managed originals/history until explicitly deleted; no automatic expiry. Before dataset-wide deletion or bulk replacement, offer a recovery snapshot and disclose its location, contents and retention. The user may decline the snapshot or include existing managed backups in the deletion scope. Never silently create or retain a copy contrary to the deletion request. Explain affected managed records/files; preserve external originals outside the managed dataset.
- Do not delete the user's external original files. Do not promise secure erasure of operating-system backups or unowned copies.
- Recovery/export must retain linked account, source, coverage and correction context, not merely a transaction list. Mechanism belongs to design.

### ING-013 — Local access and untrusted inputs

Access only the selected dataset, managed sources and explicitly supplied files within applicable permissions. Do not transmit statement data externally as part of this feature.

- **Positive:** operations identify the dataset in use, keep routine summaries to aliases and necessary details, and preserve full source evidence only in managed records.
- **Negative:** do not scan unrelated folders, execute document macros/formulas or treat embedded document text as instructions.
- Account identifiers must not unnecessarily appear in routine logs or user summaries.
- “Local SQLite/extraction” is not a claim that the host model/runtime processes data locally. Disclose relevant runtime handling rather than promising unsupported isolation.
- File permissions, defensive parsing and recovery mechanisms remain design/security-review responsibilities.

### ING-014 — Distribution and capability boundary

Document invocation, supported formats, required inputs, dataset selection, outcomes, uncertainty and missing extraction dependencies.

- Reuse installed document capabilities without assuming packages are preinstalled on every target harness.
- **Positive:** a missing extraction dependency produces an actionable outcome; existing stored data remains usable.
- **Negative:** do not run a repository service, change installer copy logic, silently install dependencies or start downstream skills as part of ingestion.
- Repository Python work follows actual `pyproject.toml` minimum **Python >=3.13**; AGENTS.md's 3.12+ summary is stale.
- Do not require changing existing PDF/XLSX frontmatter or force spreadsheet output to satisfy the current XLSX trigger. Integration must reuse extraction capability within the authorised feature boundary.

## User journey and priorities

1. Select/reuse the personal dataset and supply files.
2. Import supported content, retain originals and record per-file outcomes.
3. Resolve only material account/date/currency ambiguities; other successful imports remain available.
4. View ingestion summary, account coverage/gaps, balances/reconciliation status and unresolved observations.
5. Supply further files or corrections; resume later from durable records.

All ING requirements are baseline. Proposed defaults above are concrete decisions included in requirements approval; they are not already-approved user answers. No unresolved discovery preference requires another question before presenting this proposal.

## Verification and evidence

Later verification must use synthetic fixtures spanning all three formats, multiple accounts/cards/currencies, exact-money edge cases, empty periods, disjoint/overlapping ranges, ambiguous imports, legitimate repeated purchases, corrected sources, per-file failure and interrupted persistence. No real financial statement is required for acceptance.

Sources inspected: approved [backlog](../product-backlog.md), [lifecycle](bank-ingestion-lifecycle.md), [Product Owner plan](bank-ingestion-requirements-product-owner-plan.md), [PDF skill](../../skills/pdf/SKILL.md), [XLSX skill](../../skills/xlsx/SKILL.md), [requirements-analysis skill](../../skills/requirements-analysis/SKILL.md) and [pyproject.toml](../../pyproject.toml). No scripts/tests run and no extraction or recovery capability demonstrated.

Scope coverage: formats/reuse ING-001/014; SQLite/originals ING-002; source fields/unknowns ING-003; exact money ING-004; accounts/cards/settings ING-005; balances/reconciliation ING-006; interval inventory/gaps ING-007/008; batch failures ING-009; reimport/overlap ING-010; corrections ING-011; retention/recovery ING-012; privacy/access ING-013. All approved BL-001 scope paragraphs are represented without starting downstream features.

**Approval target:** BL-001 scope 8, requirements revision 3, ING-001–ING-014 and explicitly marked defaults. Approval permits the next applicable design stage, not implementation.

## Revision history

- 2026-10-26 — Revision 1 proposal from Product Owner PLAN-BANK-001 r1. Coordinator persisted all 14 requirements and coverage evidence. Pre-presentation refinement to ING-012 replaces automatic retained recovery copies with a disclosed, optional snapshot that respects deletion intent; Product Owner confirmed replacement wording. No other requirements changed and no approval inferred.

- 2026-10-26 — Revision 2 proposal: user requested explicit same-file and monthly/yearly overlap protection. Product Owner PLAN-BANK-001 r2 replaced ING-010 only with file-repeat/cross-source identity/provenance/multiplicity/retry rules and ING-010-A–J. Prior unapproved [revision 1 proposal](bank-ingestion-requirements-revision-1-proposal.md) preserved. Other requirements/defaults unchanged; no approval, design, code or runtime tests.

- 2026-10-26 — Revision 3 proposal: user requires header-only statement-period extraction and user clarification when dates are absent/ambiguous. Product Owner PLAN-BANK-001 r3 replaced ING-007 and clarified ING-008: inactivity is not missing coverage. Eight acceptance cases added; all other requirements including ING-010 unchanged. Unapproved [revision 2 proposal](bank-ingestion-requirements-revision-2-proposal.md) preserved; no approval/design/code/tests.

- 2026-10-26 — APR-ING-REQ-003: user explicitly approved requirements revision 3. No requirement text or defaults changed; next applicable stage architecture.
