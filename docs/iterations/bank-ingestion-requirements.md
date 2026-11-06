# BL-001 ingestion requirements — revision 4

Date: 2026-11-03. Assignment: PLAN-BANK-001 r4. Backlog revision 8, BL-001 scope revision 8. **Status: approved under APR-ING-REQ-004**, user message “yes, approved.”, 3 November 2026. Approved requirements revision 3 and APR-ING-REQ-003 remain in the [approved copy](bank-ingestion-requirements-revision-3-approved.md). APR-ING-REQ-004 approves revision 4, ING-001–ING-014, the header-date rules, ING-010-A–N and stated defaults. Architecture revision 2 later received approval APR-ING-ARCH-002. Detailed design and code still need separate approval.

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

Before a standard import, compare the statement header dates, or dates supplied by the user, with completed, verified coverage for the same account and the same statement scope. Check coverage from earlier imports and completed imports in the same batch. Do not use failed, partial or uncertain imports as proof of complete coverage. A statement for one card does not establish full-account coverage. If account, scope or dates are unclear, ask the user. Continue extraction of usable data, but keep coverage unconfirmed.

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

An “already represented” outcome may result from a completed repeat file or a fully covered account/date range. State the reason and the prior coverage used. For partial overlap, report the skipped range, newly accepted range and unresolved records. Do not describe skipped transactions as individually checked.

### ING-010 — Check date ranges and prevent repeated imports

Keep accepted records unchanged unless the user requests a correction under ING-011.

1. **Check the period first.** Obtain the account, statement scope and start/end dates under ING-007. Compare the period with completed, verified coverage for that account. Do not use filenames, transaction dates or statement frequency to establish the period.
2. **Fully covered period.** If verified coverage includes the full incoming period, stop the standard transaction import and report “already represented.” This applies when one prior range or several prior ranges cover the period. Record the upload outcome and the coverage used. Do not add transactions, balances or extra coverage from the skipped import.
3. **Partly covered period.** Accept new data only for the uncovered part. Compare transaction records across the overlap as needed to prevent repeated entries and detect conflicts. Do not add transactions from the covered part through a standard import. Keep conflicts for review under ING-011. If the available dates do not let the system assign a record safely to a covered or uncovered part, keep it unresolved and ask for clarification.
4. **Separate accounts and statement scopes.** Coverage for another account must not block import. A card-only statement must not block a full-account statement. Apply a range stop only when the prior completed coverage establishes that it includes the incoming account and statement scope.
5. **Repeat files and retries.** Use file content checks, not filenames, to recognise exact repeats. A completed repeat with no unresolved work adds no records. Failed, partial and interrupted imports remain eligible for retry. A changed file with the same name still requires the range check.
6. **Transaction checks.** Where import work remains, use a reliable account-specific provider transaction reference when available. Otherwise compare available dates, exact signed amount, currency, description and supported card information. These values are matching evidence, not a unique transaction key. Preserve separate legitimate purchases with identical values. Do not use row numbers or filenames to match transactions across files.
7. **Corrections and changes.** Explicit correction or replacement requests use ING-011 instead of the standard range stop. Do not apply changed amounts, pending-to-posted changes or new records in an already covered period automatically. Preserve source evidence and ask when the change is unclear. Do not treat refunds as duplicates merely because other values match.
8. **Safe retry.** Save accepted records, source links and import progress consistently. After an interruption, retry only unfinished work without adding accepted transactions again. Mark coverage complete only after the relevant import work completes.

**Acceptance criteria**

| ID | Case and required result |
|---|---|
| ING-010-A | Upload a completed monthly statement again, including with another filename: stop; report already represented; add no transactions, balances or coverage. |
| ING-010-B | Upload changed content with the same filename: check its account and header period. Stop a fully covered standard import; use ING-011 for an explicit correction. Do not overwrite prior records. |
| ING-010-C | Import January, then a full-year statement: skip January for new entries; accept supported new data from uncovered months. Compare overlap records where needed. Report conflicts without changing January automatically. |
| ING-010-D | Import a full year, then January for the same account and scope: stop the January standard import because its full period is covered. Do not claim its individual rows were checked. |
| ING-010-E | Two valid identical purchases occur in accepted data: retain both. Overlap checks must not reduce them to one or add them twice. |
| ING-010-F | The same provider reference appears in different accounts: do not merge their records or use one account's coverage to stop the other import. |
| ING-010-G | Matching values do not prove the same transaction: keep the match unresolved; do not remove valid records. |
| ING-010-H | New evidence suggests a pending-to-posted change or changed amount in a covered period: use ING-011 or request clarification; do not add a second completed transaction automatically. |
| ING-010-I | An import stops after some work completes: allow retry, preserve completed work and add no repeated transactions. A partial outcome must not block the retry as fully covered. |
| ING-010-J | A standard upload has a fully covered period: stop even if its content differs. If the user requests a missing-transaction check or correction, use ING-011. |
| ING-010-K | Two files in one batch cover the same account and period: after the first completes, use its verified coverage to stop the second standard import. If the first fails or remains partial, do not stop the second on that basis. |
| ING-010-L | Prior coverage contains a gap inside the incoming period: accept only supported new data for that gap; do not call the whole period already represented. |
| ING-010-M | Prior data covers another account or only a card subset: do not stop the full-account import on that basis. |
| ING-010-N | Header dates or account/scope are unclear: ask the user; do not infer them or apply a range stop. |

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

**Approval target:** BL-001 scope 8, requirements revision 4, ING-001–ING-014, ING-010-A–N and explicitly marked defaults. Approval permits the next applicable design stage, not implementation.

## Revision history

- 2026-10-26 — Revision 1 proposal from Product Owner PLAN-BANK-001 r1. Coordinator persisted all 14 requirements and coverage evidence. Pre-presentation refinement to ING-012 replaces automatic retained recovery copies with a disclosed, optional snapshot that respects deletion intent; Product Owner confirmed replacement wording. No other requirements changed and no approval inferred.

- 2026-10-26 — Revision 2 proposal: user requested explicit same-file and monthly/yearly overlap protection. Product Owner PLAN-BANK-001 r2 replaced ING-010 only with file-repeat/cross-source identity/provenance/multiplicity/retry rules and ING-010-A–J. Prior unapproved [revision 1 proposal](bank-ingestion-requirements-revision-1-proposal.md) preserved. Other requirements/defaults unchanged; no approval, design, code or runtime tests.

- 2026-10-26 — Revision 3 proposal: user requires header-only statement-period extraction and user clarification when dates are absent/ambiguous. Product Owner PLAN-BANK-001 r3 replaced ING-007 and clarified ING-008: inactivity is not missing coverage. Eight acceptance cases added; all other requirements including ING-010 unchanged. Unapproved [revision 2 proposal](bank-ingestion-requirements-revision-2-proposal.md) preserved; no approval/design/code/tests.

- 2026-10-26 — APR-ING-REQ-003: user explicitly approved requirements revision 3. No requirement text or defaults changed; next applicable stage architecture.

- 3 November 2026 — Proposed revision 4: the user asks for header dates to be checked against saved coverage before a repeat import. The Product Owner changes ING-007/009/010 and cases A–N. A standard import now stops for a fully covered period. This replaces revision 3's instruction to inspect all covered periods. Explicit corrections still use ING-011. Approved revision 3 remains in its saved copy. No new research, design or code. Requirements approval remains necessary.

- 3 November 2026 — APR-ING-REQ-004: the user approved requirements revision 4. The approval includes the date-range check and cases A–N. No requirement text changed. Next, update the architecture.
