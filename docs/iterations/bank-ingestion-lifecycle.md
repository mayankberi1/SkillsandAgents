# Bank ingestion lifecycle

Lifecycle revision 1; 2026-10-26. User request: `/plan next`; interpret short `next` as next approved backlog item. Backlog baseline revision 8, APR-BANK-008. Selection pending Product Owner verification; no active feature at baseline. No requirements, architecture, solution or iteration approval exists.

## Records

- [Product Owner plan](bank-ingestion-requirements-product-owner-plan.md), PLAN-BANK-001 r1.
- [Coordinator plan](bank-ingestion-coordinator-plan.md).
- [Backlog](../product-backlog.md).

## Decisions and checkpoints

- Initial Product Owner checklist saved before selection inspection. Await N1 selection checkpoint, then persist selected item before requirements continuation.
- Repository preconditions: distribution collection; unrelated untracked `.idea/` and `skills/.system/` excluded. `pyproject.toml` actually requires Python >=3.13, despite AGENTS.md's 3.12+ summary; actual runtime requirements must be reconciled in requirements. No files modified beyond lifecycle records.

Next authorised action: verify queue selection; stop at explicit requirements approval before design.

## Selected state — PLAN-BANK-001 r1

Product Owner independently selected BL-001 scope8/rank1: approved r8/APR-BANK-008, Ready and unfinished, no dependencies, no prior active feature. Coordinator persisted queue mode, approved queue revision8, active BL-001 In Progress/requirements, and links before requirements continuation. No scope/rank changes. Next: N2–N4 requirements batch; no design or implementation.

## Requirements proposal checkpoint

[Requirements revision 1](bank-ingestion-requirements.md), ING-001–ING-014 plus explicitly marked operational defaults, saved from Product Owner N1–N4 handoff. Scope coverage mapping and positive/negative cases complete. ING-012 refined before presentation to respect deletion intent with optional disclosed recovery snapshots. BL-001 now Awaiting Approval at requirements; queue8 remains active and other 13 features remain Ready.

Evidence limitations: no scripts/tests or extraction/recovery capability demonstrated; generic synthetic fixtures planned for later verification. Actual pyproject Python >=3.13 reconciles stale AGENTS summary; existing PDF/XLSX extraction reuse does not require workbook output or trigger/frontmatter edits. No new scope, SQL/schema design, architecture/solution/iteration approval or implementation.

**Next required approval:** BL-001 scope8, requirements revision1, ING-001–ING-014 and proposed defaults. Only then proceed to applicable architecture/design; implementation remains unapproved.

## Requirements refinement — PLAN-BANK-001 r2

User asked explicit duplicate-import logic for repeated monthly and overlapping yearly statements. Product Owner D1–D3 refined ING-010 only; Coordinator preserved [unapproved r1](bank-ingestion-requirements-revision-1-proposal.md) and saved [requirements r2](bank-ingestion-requirements.md) with ten acceptance cases ING-010-A–J. File recognition and cross-file transaction identity are separate; provenance and legitimate multiplicity retained, uncertainties/retries explicit. No schema/SQL/code or tests.

This supersedes the preceding r1 approval target. **Next required approval: BL-001 scope8, requirements revision2, ING-001–ING-014, ING-010-A–J and explicit defaults.** Queue8 remains on BL-001 Awaiting Approval at requirements; no other item advanced.

## Header-only period clarification — PLAN-BANK-001 r3

User requires header-derived start/end only, with explicit user answer for missing/ambiguous boundaries; transaction inactivity must not imply missing coverage. Product Owner H1–H3 returned ING-007 replacement/eight cases and ING-008 clarification. Coordinator preserved unapproved r2 and saved requirements r3, leaving all other requirements (including overlap rules) unchanged.

**Current next approval: BL-001 scope8, requirements revision3, ING-001–ING-014 including header-period cases, ING-010-A–J and explicit defaults.** Queue8/BL-001 Awaiting Approval at requirements; no downstream approvals.

## Requirements approval — APR-ING-REQ-003

2026-10-26: user replied “approved” to requirements revision3. Approval covers ING-001–ING-014, header-period cases, ING-010-A–J and defaults exactly as saved; no content changes. Prior approval-pending statements above are historical. Coordinator recorded approval in requirements/backlog and advanced BL-001 In Progress/architecture, retaining active queue8. No architecture, solution/UI design, iteration or implementation approved.

Next: Architect assesses material boundaries/alternatives from approved requirements; present a separate architecture approval proposal before solution design.

Architecture assignment ARCH-BANK-001 r1, [Architect plan](bank-ingestion-architect-plan.md): initial five-task checkpoint persisted/acknowledged before evidence inspection. No architecture result or approval yet. Existing inputs remain fixed; next batch ARCH-001/002 only.

Architect evidence checkpoint saved: ARCH-001/002 done; requirements approval/state consistent. Reuse installed extraction capabilities, no workbook recalculation/save/vendoring; dependencies not bundled by assumption; Python >=3.13 actual. Source licenses remain unchanged. No code/runtime trials. Next batch ARCH-003/004 primary-doc research/alternatives/proposal, then coverage reconciliation.

## Architecture proposal checkpoint

[Architecture revision1](bank-ingestion-architecture.md), ARCH-D01–D06 and material dependency/security boundaries saved from final Architect ARCH-001–005 handoff. Alternatives and full ING-001–014/ING-010-A–J trace reconciled. XML protection fail-closed and diagram shared-boundary clarification confirmed by Architect before presentation. Technical sources inspected, but parsing, matching, compatibility, recovery and security behaviour remain unverified until implementation/testing.

BL-001 Awaiting Approval at architecture; queue8 remains active, others13 Ready. **Next explicit approval: architecture revision1, ARCH-D01–D06 plus dependency/security boundaries.** Approval permits solution design, not schema/API implementation or development. No solution/UI design, iteration or code yet.

## Plain-language edit — 3 November 2026

The Coordinator rewrote the architecture document in simple language at the user's request. The original wording remains in `bank-ingestion-architecture-revision-1-original-wording.md`. The decisions and approval request remain unchanged. BL-001 still awaits approval of architecture revision 1. No code changed.

## Date-range check — 3 November 2026

The user requests a header-date check against saved coverage before importing the same period again. Product Owner PLAN-BANK-001 r4 proposes changes to ING-007/009/010 and cases A–N. The Coordinator saved [requirements 4](bank-ingestion-requirements.md) and kept [approved requirements 3](bank-ingestion-requirements-revision-3-approved.md).

The proposed rule stops a standard import when completed coverage includes its full period. For partial overlap, it accepts new data only for gaps. It preserves retries, account/card limits and explicit corrections. This changes the earlier rule to inspect every covered period.

BL-001 awaits requirements revision 4 approval. Architecture revision 1 needs an update after that approval. No design or code work may advance from the old proposal. Queue 8 and all item ranks remain unchanged.

## Requirements 4 approval — 3 November 2026

The user replied “yes, approved.” Approval APR-ING-REQ-004 applies to requirements revision 4, ING-001–014, the header-date rules, ING-010-A–N and defaults. The Coordinator recorded approval and set BL-001 In Progress at architecture. Update the architecture before seeking its separate approval. Queue 8 stays active on BL-001. No code changed.

## Architecture revision 2 — 3 November 2026

Architect ARCH-BANK-001 r2 returned changes to decisions D03–D05 and the diagram. The Coordinator saved [architecture revision 2](bank-ingestion-architecture.md). It checks completed coverage before a standard import, stops fully covered imports, and accepts new data only for gaps. It keeps retries and explicit corrections available. It includes completed imports in the same upload.

The other decisions and file/software/privacy rules remain unchanged. The previous architecture remains in its saved copy. All cases ING-010-A–N have a matching design rule. No code, research or tests. BL-001 awaits approval of architecture revision 2, ARCH-D01–D06 and the stated software/file/privacy rules. Detailed design remains separate.

## Architecture approval — 3 November 2026

The user replied “approved.” Approval APR-ING-ARCH-002 applies to architecture revision 2, decisions ARCH-D01–D06 and the software, file and privacy rules. The Coordinator recorded approval without changing those decisions. BL-001 now continues at solution/UI design. No new screen is planned. Prepare the table and command design for separate approval. Queue 8 stays active. No code changed.

Detailed design assignment DESIGN-BANK-001 r1: the Coordinator saved the [initial plan](bank-ingestion-solution-designer-plan.md) before the specialist reads the project files. First inspect approved inputs and report evidence. Save that record before defining the design.

The Coordinator saved the evidence record. SD-01 and SD-02 are complete. The specialist confirmed requirements 4, architecture 2 and Python 3.13. Earlier approval summaries are historical. No tested file reading or recovery exists yet. The next work defines records, commands, failure handling and checks against the approved rules.

## Detailed design proposal — 3 November 2026

The Coordinator saved [detailed design revision 1](bank-ingestion-solution.md). The designer defined records, installed files, commands, exact amounts, source evidence, range checks, recovery and file limits. Review corrections added complete setup and answer paths, extraction-run checks, precise revisions, preview/apply rules and full deletion scope. Unknown-period entries remain available but do not count until required checks pass.

All 14 requirements and cases A–N have design references. The designer checked five code-organisation principles without adding unnecessary classes. No new screen, private statements, code or runtime tests. Technical sources were checked, but software behaviour remains unproven.

BL-001 awaits approval at solution/UI design. Queue 8 remains active; other 13 items remain Ready. **Next approval: detailed design revision 1, including records, commands, proposed limits and diagrams.** Approval permits iteration planning, not implementation.

## Short design copy — 3 November 2026

The user first asked for a shorter document with diagrams, tables and short rules. An earlier edit used a short copy and a separate reference. The user then asked for one file. The combined document below supersedes that format. No code changed.

## Single design document — 3 November 2026

The Coordinator combined the design into [one document](bank-ingestion-solution.md), using diagrams, tables and bullets. It retains the record fields, commands, request rules, limits, recovery steps and approval request without repeated explanations. The Coordinator removed the separate reference file as requested. No decision or approval status changed. Detailed design revision 1 still awaits approval.

## Smaller first version — 3 November 2026

The user requested fewer parts, not only shorter wording. The Coordinator saved and confirmed DESIGN-BANK-001 r2 before specialist review. The specialist returned eight tables, five main commands and two Python files, replacing 18 tables, 22 commands and seven Python files. Saved plans, request tracking and row-group saves are removed. The Coordinator checked the date-range rules, source links, partial retries, exact money, protections, corrections and deletion scope, and saved [design revision 2](bank-ingestion-solution.md) in the same file. Requirements 4 and architecture 2 remain unchanged. No code, runtime tests or new research. BL-001 remains Awaiting Approval at solution/UI design; other 13 items remain Ready. Next: approve design revision 2 before iteration planning.

## Record and function clarification — design revision 3

The user accepted clarification of statement records, accepted transactions and function steps. The Coordinator saved and acknowledged DESIGN-BANK-001 r3 before specialist continuation. C3-01–04 completed. [Design revision 3](bank-ingestion-solution.md) keeps eight tables and two Python files, uses `statement_records` for original observations and `transactions` for accepted reporting fields, and defines four import/read functions plus eight required supporting functions. Saving repeats all checks against current history. Four examples describe proposed behaviour; no tests ran. Requirements 4 and architecture 2 remain unchanged. No code or new research. BL-001 remains Awaiting Approval at solution/UI design; next approval is design revision 3, permitting iteration planning only.

## Design approval — 3 November 2026

The user replied “approved” to design revision 3. APR-ING-DES-003 records this approval. The Coordinator updated the design and backlog. BL-001 is In Progress at iteration planning; queue 8 and the other 13 items remain unchanged. No iteration or development approval exists. Product Owner assignment ITER-BANK-001 r1 will return an initial plan before inspecting the baseline and proposing increments.

## Iteration proposal — 3 November 2026

Coordinator saved and acknowledged the Product Owner's initial plan before inspection. ITER-BANK-001 r1 completed I1–I3 and returned [three implementation steps](bank-ingestion-iterations.md), revision 1. The Coordinator checked scope, dependencies, approved requirements, file lists and independent checks. Tests stay outside distributed skill files. No code, test runs or new research. BL-001 awaits step 1 approval at iteration planning. The other 13 items remain Ready. Approval of step 1 will not approve steps 2–3 or another feature.

## Inline library declarations — 3 November 2026

The user requested a design and plan update after discussing inline Python library lists and uv. Coordinator saved and acknowledged DESIGN-BANK-001 r4 before the specialist read the documents. P4-01–03 completed. [Design 4](bank-ingestion-solution.md) keeps design 3's approved data and behaviour, adds inline Python/library declarations with normal imports, and requires explicit uv preparation. [Iteration plan 2](bank-ingestion-iterations.md) removes the proposed requirements.txt file and adds corresponding setup checks. Missing software is reported; imports and statement reads install nothing and use no network. Official Agent Skills and uv guidance were checked, but no software ran. No source files changed. The earlier design approval remains APR-ING-DES-003; this user-requested update grants no implementation approval. BL-001 still awaits step 1 approval. Other item states and queue 8 remain unchanged.

## Step 1 approval — 3 November 2026

The user replied “approved.” APR-ING-IT1-001 approves step 1 in iteration plan revision 2 only. Coordinator recorded approval and set BL-001 In Progress at implementation. Developer assignment DEV-BANK-001 r1 must return its initial checklist, then a baseline checkpoint, before implementation. Allowed source files: skills/bank-statement-ingestion/scripts/bank_history.py and tests/bank_statement_ingestion/test_bank_history.py. No document reader, skill instructions, external libraries or step 3 maintenance in this step. Independent tests and code/security reviews remain required. Steps 2–3 and other backlog items remain unapproved.

## Step 1 developer handoff

Coordinator saved DEV-BANK-001 r1 baseline before authorising implementation. Developer returned two new files: bank_history.py and test_bank_history.py. Reported 33 tests plus 7 subtests pass on Python 3.14.4 and both files compile; ruff unavailable. Source evidence remains caller-supplied until the separately approved reader step. The foundation is not a complete installed skill. Coordinator saved the handoff and advanced BL-001 to testing. TEST-BANK-001 r1 will independently inspect actual files and acceptance/failure cases after its checklist is saved. No approval for later steps.

## Independent test failure and repairs

TEST-BANK-001 r1 independently passed 33 existing tests and compilation but found four defects in additional checks: amount substring/sign evidence, text acting as boolean, malformed header-date substrings and loss of valid partial work on an invalid record date. Result Failed. Coordinator saved the findings and DEV-BANK-001 r2 F1–F5 before authorising fixes in the same two files. BL-001 is Blocked at testing until fixes and independent retests pass. Stale design statements about absent code/approval were corrected. No scope expansion or later-step approval.

## Independent retest — TEST-BANK-001 r2

Developer repaired four defects and added regression cases within the same two files. Coordinator saved repair and retest checklists before continuation. Tester independently confirmed 37 suite tests, four original reproduction checks and compilation pass. ruff remains unavailable. All earlier failures remain recorded. BL-001 returns to In Progress at reviews; step 1 is not complete until code and security reviews pass. REVIEW-BANK-001 r1 will inspect correctness and unnecessary complexity after its checklist is saved.

## Step 1 complete — 3 November 2026

Code review reproduced three more defects: money settings changed meaning on unit changes; exact repeats removed reconciliation; covered references ignored date conflicts. Coordinator saved reproduction/repair plans before fixes. Developer repaired these in the same two files. Tester independently confirmed 41 suite tests, four original and three separate review-repair checks, compilation and unchanged final source/test hashes. Code/simplicity review Passed after full base and repair diff review. Security review Passed for all 13 changed paths with no findings. Reviewers used complete supplied artifacts because permitted local readers were unavailable; Tester verified disk hashes. Security document verdicts cover current content, without an original document comparison. ruff was absent and did not run.

Coordinator saved all final checkpoints before closing step 1. Production hash 90a3fb3266cdb319b1269bb05047b78b29835ca7f884c1bf8aebbefe897254f1; test hash d8c97c8224bce93f7ae5f00d7a218aa7bc937a435d16f50f3084fdfabb029677. Complete history helper is a tested foundation using caller evidence, not a reader or finished installed skill. BL-001 remains Awaiting Approval at iteration planning for step 2 only. Queue 8, scope/ranks and other 13 Ready items remain unchanged. Step 3 remains unapproved. Final documentation changes record these established results and the next decision; no source changes after final hash checks.

## Step 2 approval — 3 November 2026

The user replied “yes” to step 2 approval. APR-ING-IT2-001 covers file reading, inline library declarations, explicit setup checks and the five source/test paths in iteration plan 2. Coordinator recorded approval, restored BL-001 In Progress at implementation, and saved DEV-BANK-002 r1's initial checklist before baseline inspection. Developer must return baseline/library evidence before edits. Step 3 and normal user installation remain unapproved. Other item scopes/ranks and queue 8 remain unchanged.

## Step 2 implementation and first independent check

Coordinator saved baseline and minimal setup decision before implementation. Existing PDF tools plus defusedxml 0.7.1 were selected within approved architecture; necessary temporary development setup was announced and recorded under step 2 approval. Sandbox DNS failed; native authorised escalation completed /tmp-only setup. No normal user/project setup changed. Developer returned five scoped files with 70 tests/46 subtests, earlier seven probes and compilation passing. Standard XLSX dates/scientific amounts preserve raw text; unknown styles/layouts remain unresolved. POSIX controls required; missing mandatory controls fail closed.

TEST-BANK-002 r1 independently reproduced the passing suite/probes and real imports/cleanup but found P1 date-role proof failure: a date cell could fill both dates or a Posting date cell could invent a transaction date. Coordinator saved failed evidence and DEV-BANK-002 r2 repair checklist before authorising fixes. BL-001 Blocked at testing until independent retest passes. Reduced limit tests are not maximum-size stress tests; Python socket checks are not host network isolation. ruff unavailable. No step 3 approval.

## Step 3 approval — 4 November 2026

The user asked to “continue with step 3 development”. Coordinator recorded APR-ING-IT3-001 for the saved scope: corrections, recovery, export/restore/deletion, skill instructions, catalogue updates and checks for ING-001–014. The security recheck found that the current `bank_history.py` contains step 3 work that the frozen step 2 tests and reviews do not cover. Developer must preserve that work, complete the approved step 3 scope, and return the actual combined source for tests and independent reviews. Step 3 is approved for development; no completion claim is made.
## BL-001 completion — 4 November 2026

Under APR-ING-IT3-001, the Coordinator completed Step 3 after independent checks passed. Tester r4 reports 122 tests and 69 subtests passed and compilation passed. Code review r4 and security review r2.1 passed. The final security record confirms the path, permission and account-visibility repairs. Earlier step 2 review statuses apply only to the frozen step 2 source; step 3 reviews cover the current combined source. BL-001 is Done. Queue revision 8 and all other ranks and scopes remain unchanged. No next item is active.

## Format design revision 5 — 5 November 2026

The user approved solution design revision 5 as APR-ING-DES-006. It replaces fixed date/amount keys with string variables, uses Python date parsing/formatting and exact Decimal conversion, and stops the whole statement on a date or amount format failure. The Coordinator recorded BL-001 scope revision 9 and saved the [step 4 implementation proposal](bank-ingestion-iterations.md#step-4-proposal--flexible-field-formats). Source, sign, ambiguity and history protections remain in scope. No code changed.

**Step 4 approval:** APR-ING-IT4-001, user “approved” on 5 November 2026. The Coordinator recorded the approval and moved BL-001 scope revision 9 to In Progress at implementation. The approved queue revision and ranks remain unchanged. The Developer checklist and code work are now in progress; independent testing, code review and security review remain required before completion.

### 5 November 2026 — format review findings

Independent review found that amount separators can have more than one valid meaning without an evidence check. It also found that an Excel serial can use the wrong workbook epoch when the protected reader does not return canonical date evidence. The Code Reviewer also found one overlap test fixture that stopped before the intended check and one error that could report the amount cell for a date failure. The Security Reviewer found overly broad separator characters and no date-pattern length cap; the Developer fixed those two input checks and added tests.

The Solution Designer proposed design revision 6: carry and check amount-format evidence; expose the reader's Excel epoch and reject a mismatch before writing statement data. The user replied “approved both”; the Coordinator recorded APR-ING-DES-007. The user then approved the revised step 4 plan as APR-ING-IT4-002. BL-001 is In Progress at implementation. Independent checks passed for the date error location and overlap fixture fixes. The remaining implementation and full reviews are in progress. No next backlog item is active.

### 5 November 2026 — BL-001 scope revision 9 complete

The Developer completed APR-ING-IT4-002 and the approved repairs. The amount parser requires checked evidence when the value has more than one valid meaning. The protected XLSX reader reports its workbook epoch. The history check rejects a mismatch and requires the styled canonical date when present. Malformed format records and duplicate workbook epoch fields fail before writes. The test folder is now visible to Git only for `tests/bank_statement_ingestion/`.

The Coordinator ran all five bank statement test files: 157 tests and 166 subtests passed. Compilation and `git diff --check` passed. Ruff is unavailable. Code review and security review passed after repairs. No real history or statement was used, and no install occurred. BL-001 scope revision 9 is Done. No next item was selected.

