# Product backlog

Revision: **76 (BL-016 coding in progress)**. Date: 2026-11-17. Execution mode is `queue`; approved queue revision **15** includes BL-001, BL-009 and BL-016–BL-032, with prior ranks retained. Active item: **BL-016**, In Progress at coding. BL-001, BL-009 and BL-015 are Done. BL-006, BL-007 and BL-010 are retired. Twelve separate analysis and coordination items are retired; their useful on-demand behavior remains in the financial-history skill. See [retired item archive](iterations/retired-backlog-items-revision-10.md), [BL-010 lifecycle](iterations/bl-010-account-consolidation-lifecycle.md), [BL-006 lifecycle](iterations/bl-006-analysis-lifecycle.md), [BL-007 lifecycle](iterations/bl-007-banker-lifecycle.md), and [BL-009 lifecycle](iterations/bank-tagging-lifecycle.md). BL-015 requirements, architecture, design, coding and checks remain complete under APR-DB-REQ-005, APR-DB-ARCH-005, APR-DB-DES-005, APR-DB-IT-001 and APR-DB-CODE-001.

Execution mode: `queue`. **Active item: BL-016.** Approved queue revision **15** includes BL-001, BL-009 and BL-016–BL-032, with prior ranks retained. **BL-016 is In Progress at coding; BL-017–BL-032 are Ready. BL-001, BL-009 and BL-015 are Done; BL-006, BL-007 and BL-010 are retired.** See [BL-009 lifecycle](iterations/bank-tagging-lifecycle.md). Skills are not installed in a user harness. No real history or statement was used.

## Direction and confirmed decisions

User `/backlog` request: add skills that ingest bank statements using existing document skills and analyse duplicate, unusual and recurring transactions and spending.

User discovery answers: first version supports **text PDFs and CSV/XLSX**; scanned statements are deferred. Audience: **personal bank and credit-card accounts**. Keep currencies separate.

User expansion: save reusable data across sessions; accept statement top-ups each month; generate updated reports understandable to an ordinary person across **savings, transaction and credit-card accounts**. Monthly refresh is invoked when files are supplied; unattended schedules/notifications have not been requested.

Latest clarification supersedes any monthly-statement assumption: statements may have arbitrary or changing frequency, including custom/ad hoc exports. Coverage is based on date ranges per account, never document counts. Monthly reporting remains a possible review cadence, not an input requirement. User proposes a distributed `banker` subagent that invokes ingestion and separate Python-backed analysis/report skills, requests missing date ranges, and synthesises findings into suggested actions and an executive summary.

User now confirms: **analyse available data immediately and label gaps**, maintaining a persistent inventory for every account and date range. Completeness is not a prerequisite for analysis. User also requests projected balances and negative-balance warnings using balances and historic mortgage, bill and subscription payments.

User further confirms: accept **multiple files at once**; Banker runs in its **own working context**, returning only summary reports and an executive summary to the main chat; use an **adjustable 30-day forecast outlook**. Context isolation is intended behaviour to verify later, not a demonstrated runtime or privacy guarantee.

2026-11-17 Google service skills direction: user proposes naming the existing Gmail skill `gmail`, then adding separate skills for Calendar, Drive, Tasks and Contacts. The user asks to split Gmail attachments, organization and writing into separate backlog items, then proposes service-level skills, then asks to split every service further into distinct tasks. Revision 70 replaces the earlier broad proposed entries with service-specific task items. User approved revision 70 on 2026-11-17. BL-016–BL-032 are Ready under approved queue revision 15; this does not approve their requirements or later stages.

Historical discovery choices: selected output was **executive summary plus detailed report**, without a required Excel workbook. The user requested a **user-set safety buffer per funding account**, separate backlog items for extras, a transaction-tagging skill, and account/card consolidation. Later review in queue revision 10 retires the separate analysis items and keeps on-demand analysis in the financial-history skill.

2026-10-25 clarification: unsuccessful/ambiguous vendor lookup must ask the user to classify the affected transactions and retain reusable classifications for future tagging. User proposes shared transactions/accounts/tagging tables used by reporting scripts. These record groups are the starting point for storage brainstorming; database engine, detailed schema, original-file retention and deployment remain unselected.

**Final choices, 2026-10-26:** user answered `1A, 2A, 3A, generic initially`: one local personal SQLite dataset; retained original copies in a source folder alongside the database; all 14 capabilities were initially prioritised; generic text PDF/CSV/XLSX support initially. Queue revision 10 later retires nine analysis items as separate features. Vectors are not selected or required. Generic support is not a claim that every bank layout parses correctly; ambiguous/unsupported inputs remain explicit. The approved design and implementation define the schema and operations; tests verify the planned cases with generated data.

Latest scope refinements below govern where older revision paragraphs conflict. Python handles statement import and database writes. The financial-history skill directs on-demand analysis from saved data. Banker remains separate harness work.

These are distributed skills, not a banking service. Reuse existing PDF and spreadsheet skills for extraction and requested reports. Source files, not bank connections, are the input. The financial-history skill reads the saved records and states data limits.

Across all analyses retain account context and separate currencies: duplicate comparisons use account/currency context, unusual-transaction baselines use relevant personal-account history within each currency, and recurring groups retain account context. Consolidated spending explicitly handles transfers and repayments.

## Active backlog — queue revision 15

| ID | Rank | Title | Scope revision | Status | Stage | Dependencies |
|---|---|---|---|---|---|---|
| BL-001 | 1 | Persistent ingestion, account/card inventory and coverage | 9 | Done | complete | None |
| BL-009 | 2 | Transaction tagging and merchant identification skill | 2 | Done | complete | BL-001 |
| BL-015 | 15 | Expose database CRUD operations to the LLM | 5 | Done | complete | BL-001 |

### Approved queue — revision 15

| ID | Rank | Title | Scope revision | Status | Stage | Dependencies |
|---|---:|---|---:|---|---|---|
| BL-016 | 16 | Name the existing skill Gmail | 3 | Awaiting Approval | solution design | None identified |
| BL-017 | 17 | Retrieve Gmail attachments | 1 | Ready | requirements | None identified |
| BL-018 | 18 | Organize Gmail messages | 1 | Ready | requirements | None identified |
| BL-019 | 19 | Write Gmail messages | 1 | Ready | requirements | None identified |
| BL-020 | 20 | Find and read Calendar events | 1 | Ready | requirements | None identified |
| BL-021 | 21 | Create and change Calendar events | 1 | Ready | requirements | None identified |
| BL-022 | 22 | Cancel events and manage invitations | 1 | Ready | requirements | None identified |
| BL-023 | 23 | Find and inspect Drive files | 1 | Ready | requirements | None identified |
| BL-024 | 24 | Download and export Drive files | 1 | Ready | requirements | BL-023 |
| BL-025 | 25 | Add files to Drive | 1 | Ready | requirements | BL-023 |
| BL-026 | 26 | Organize and share Drive files | 1 | Ready | requirements | BL-023 |
| BL-027 | 27 | Find and read Google Tasks | 1 | Ready | requirements | None identified |
| BL-028 | 28 | Create and update Google Tasks | 1 | Ready | requirements | BL-027 |
| BL-029 | 29 | Complete and remove Google Tasks | 1 | Ready | requirements | BL-027 |
| BL-030 | 30 | Find and read Google Contacts | 1 | Ready | requirements | None identified |
| BL-031 | 31 | Add and update Google Contacts | 1 | Ready | requirements | BL-030 |
| BL-032 | 32 | Delete Google Contacts | 1 | Ready | requirements | BL-030 |

### Gmail

#### BL-016 — Name the existing skill Gmail
- Problem: `skills/google-workspace` only supports Gmail, but its name suggests broader Google service support.
- Intended outcome: name the existing skill `gmail` and retain its current sign-in, search, read and label features.
- Approved scope revision 3: rename the skill and update its references. Preserve existing sign-in access.
- Evidence: direct user direction, 2026-11-17. Repository inspection found the existing skill, scripts, tests, setup notes and keyring service name use `google-workspace` or `google-workspace-gmail`.
- Dependencies: none. Rank 16 is in approved queue revision 15.
- Confirmed decision: user wants existing users to keep their saved Gmail sign-in after the rename. Keep the current keyring service/account entry, including the `google-workspace-gmail` service name.
- Requirements proposal (GMR-001–GMR-006):
  - **GMR-001:** The skill folder and frontmatter name are `gmail`.
  - **GMR-002:** The renamed skill retains authentication setup, status and revoke, Gmail search, message retrieval, label listing, and confirmed single-message label changes.
  - **GMR-003:** Existing saved credentials remain available through the same keyring service and account entry. Users do not need to repeat Google consent only because of the rename.
  - **GMR-004:** The existing scope remains unchanged after the rename. The rename does not request wider Gmail access.
  - **GMR-005:** The catalog and active user instructions use the new `gmail` skill name and folder path. They explain that the retained keyring entry still uses `google-workspace-gmail`.
  - **GMR-006:** The generic installers continue to copy the renamed skill directory. This item does not change installer scripts or remove copies already installed in external harnesses.
- Acceptance evidence planned: inspect the renamed skill metadata and all repository references; confirm the keyring service name and OAuth scopes stay unchanged; run `git diff --check`. No test or runtime evidence exists. Do not run tests unless the user asks.
- Requirements approval: approved as **APR-GMAIL-REQ-001** on 2026-11-17. Approval covers GMR-001–GMR-006 only.
- Design proposal:
  - No architecture stage applies. The work renames a skill folder and updates its instructions; it adds no service, data store or new permission.
  - Rename `skills/google-workspace/` to `skills/gmail/`. Move all current files with the directory.
  - `skills/gmail/SKILL.md`: set frontmatter name and heading to `gmail` / `Gmail`; keep approved behavior and explain the retained keyring service name.
  - `skills/gmail/scripts/gmail.py`: change the command-line description to Gmail; keep command names and behavior.
  - `skills/gmail/references/setup.md`: state that the keyring name remains `google-workspace-gmail`; keep commands based on the installed skill directory.
  - `skills/gmail/references/gmail-search-syntax.md`, `requirements.txt`, `scripts/gmail_api.py`, and `tests/test_auth.py`, `tests/test_checks.py`, `tests/test_gmail.py`, `tests/test_setup.py`: move with the directory; no content or function changes are planned.
  - `skills/gmail/scripts/auth.py`: move with the directory; keep `KEYRING_SERVICE = "google-workspace-gmail"` unchanged.
  - `README.md` and `skills/CATALOG.md`: add the `gmail` skill listing and correct the README skill count. Preserve the existing unrelated edits in these files.
  - Do not change installer scripts. They copy each skill directory by its folder name. Existing copies in external harnesses are outside this item.
  - Make no changes to OAuth scopes, Gmail operations or dependencies. No new script, function, class or API is required.
- Design checks: inspect all references to the old skill name; confirm the renamed folder contains each existing tracked file; run `git diff --check` after coding. Do not run tests unless the user asks. No checks have run for this proposal.
- Design approval: approved as **APR-GMAIL-DES-001** on 2026-11-17. Approval covers the rename design only.
- Iteration plan: [BL-016 Gmail rename plan](iterations/gmail-skill-rename-lifecycle.md).
- Coding approval: approved by the user on 2026-11-17 as **APR-GMAIL-CODE-001**. Approval covers the coding plan in the lifecycle record.
- Status: In Progress; stage coding.
- History: revision 1 was a generic Gmail capability; revision 2 added everyday Gmail work; revision 3 separates the rename from the Gmail features. Revisions 68–69 record earlier proposals. User approved backlog revision 70 on 2026-11-17 and confirmed keeping current sign-in on 2026-11-17. Requirements were approved as APR-GMAIL-REQ-001; design was approved as APR-GMAIL-DES-001. Iteration approval remains separate.

#### BL-017 — Retrieve Gmail attachments
- Problem: the Gmail skill cannot retrieve message attachments.
- Intended outcome: let a user find and save an attachment from a selected message.
- Scope: list and retrieve attachments. Save location, file limits, name conflicts and file safety remain open.
- Evidence: user request, 2026-11-17. Gmail API provides an attachment retrieval method. [Gmail attachments reference](https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments).
- Dependencies: none identified. Rank 17 is in approved queue revision 15.
- Open questions: Should the skill only list and save attachments? Where may it save them, and what size or file types should it allow?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-018 — Organize Gmail messages
- Problem: the Gmail skill cannot organize messages beyond changing one label on one message.
- Intended outcome: let a user organize messages with selected Gmail actions.
- Scope: labels, filters, snooze, archive and bulk actions are candidates. Exact actions and confirmation rules remain open.
- Evidence: user request, 2026-11-17. Gmail supports message listing and label changes; Google's API reference includes label changes and filter methods. [Gmail API reference](https://developers.google.com/workspace/gmail/api/reference/rest).
- Dependencies: none identified. Rank 18 is in approved queue revision 15.
- Open questions: Which actions should be included? Should any action affect more than one message?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-019 — Write Gmail messages
- Problem: the Gmail skill cannot create email for a user.
- Intended outcome: let a user prepare email in Gmail.
- Scope: create drafts, reply, forward and send are candidates. Recipient checks and confirmation before sending remain open.
- Evidence: user request, 2026-11-17. Gmail API supports drafts and sending. [Gmail draft guide](https://developers.google.com/workspace/gmail/api/guides/drafts) and [Gmail API scopes](https://developers.google.com/workspace/gmail/api/auth/scopes).
- Dependencies: none identified. Rank 19 is in approved queue revision 15.
- Open questions: Drafts only, or also send after exact confirmation? Should replies and forwards be included?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

### Google Calendar

#### BL-020 — Find and read Calendar events
- Problem: the repository has no Calendar skill to answer a user's questions about events.
- Intended outcome: find events in a date range and show their key details.
- Scope: list and read events. Calendar selection, date range, recurring events and guest details remain open.
- Evidence: user direction, 2026-11-17. Calendar API supports event listing and event details. [Calendar events list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list).
- Dependencies: none. Rank 20 is in approved queue revision 15.
- Open questions: Which calendars and event details should the skill search?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-021 — Create and change Calendar events
- Problem: a user cannot ask a repository skill to add or change a Calendar event.
- Intended outcome: create or update an event when the user requests it.
- Scope: event creation and updates. Time zone, recurrence, guests, reminders and sending guest notifications remain open.
- Evidence: user direction, 2026-11-17. Calendar API provides event insert and update methods. [Calendar API reference](https://developers.google.com/workspace/calendar/api/v3/reference).
- Dependencies: none identified. Rank 21 is in approved queue revision 15.
- Open questions: Which event fields can the skill set, and when must it ask before notifying guests?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-022 — Cancel events and manage invitations
- Problem: a user cannot cancel an event or respond to an invitation through a repository skill.
- Intended outcome: let a user cancel selected events or manage event invitations.
- Scope: cancellation and invitation responses. Guest notifications, organizer status and recurring-event cases remain open.
- Evidence: user direction, 2026-11-17. Calendar API exposes event update and deletion methods; updates can notify guests. [Calendar update reference](https://developers.google.com/workspace/calendar/api/v3/reference/events/update) and [Calendar API reference](https://developers.google.com/workspace/calendar/api/v3/reference).
- Dependencies: none identified. Rank 22 is in approved queue revision 15.
- Open questions: Should the skill cancel events, accept/decline invitations, or both? Require exact confirmation before each change?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

### Google Drive

#### BL-023 — Find and inspect Drive files
- Problem: the repository has no Drive skill to find a user's files.
- Intended outcome: search Drive and show selected file details.
- Scope: list, search and inspect file names and metadata. Search folders and shared drives remain open.
- Evidence: user direction, 2026-11-17. Drive API supports file listing and reading metadata. [Drive API reference](https://developers.google.com/workspace/drive/api/reference/rest/v3).
- Dependencies: none. Rank 23 is in approved queue revision 15.
- Open questions: Should the first version see only user-selected files or search all files the user can access?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-024 — Download and export Drive files
- Problem: a user cannot retrieve a selected Drive file through a repository skill.
- Intended outcome: download ordinary files or export Google documents to a user-selected format.
- Scope: download and export only. Local save path, allowed formats, file size and overwrite rules remain open.
- Evidence: user direction, 2026-11-17. Drive API has download and export methods. [Drive API reference](https://developers.google.com/workspace/drive/api/reference/rest/v3).
- Dependencies: BL-023. Rank 24 is in approved queue revision 15.
- Open questions: Which file types and export formats should the skill support? Where should it save files?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-025 — Add files to Drive
- Problem: a user cannot add a local file to Drive through a repository skill.
- Intended outcome: upload a chosen file or create a Drive file.
- Scope: file upload and creation only. Destination folder, duplicate names and supported file types remain open.
- Evidence: user direction, 2026-11-17. Drive API provides file create and upload methods. [Drive file create](https://developers.google.com/workspace/drive/api/reference/rest/v3/files/create).
- Dependencies: BL-023. Rank 25 is in approved queue revision 15.
- Open questions: Which file types and destination rules should the first version support?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-026 — Organize and share Drive files
- Problem: a user cannot organize or share Drive files through a repository skill.
- Intended outcome: move or rename files and manage sharing when requested.
- Scope: moving, renaming, trashing and changing access are candidates. Exact actions, recipients and confirmation rules remain open.
- Evidence: user direction, 2026-11-17. Drive API supports file updates and permanent deletion; access scopes vary from selected files to broad Drive access. [Drive API reference](https://developers.google.com/workspace/drive/api/reference/rest/v3) and [Drive API scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).
- Dependencies: BL-023. Rank 26 is in approved queue revision 15.
- Open questions: Which organization and sharing actions should be included? Require confirmation before changing access or deleting a file?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

### Google Tasks

#### BL-027 — nd and read Google Tasks
- Problem: the repository has no Tasks skill to show task lists and tasks.
- Intended outcome: find and read a user's task lists and tasks.
- Scope: list and read only. Completed tasks and task-list selection remain open.
- Evidence: user direction, 2026-11-17. Tasks API provides task-list and task read methods. [Tasks API reference](https://developers.google.com/tasks/reference/rest/v1/tasks).
- Dependencies: none. Rank 27 is in approved queue revision 15.
- Open questions: Should the skill show completed tasks, task notes and due dates?
- Status: Ready; stage requirementFis; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-028 — Create and update Google Tasks
- Problem: a user cannot create or edit tasks through a repository skill.
- Intended outcome: create tasks and change their title, notes, due date or position.
- Scope: task creation and updates. Task list choice and date handling remain open.
- Evidence: user direction, 2026-11-17. Tasks API supports insert, update, patch and move methods. [Tasks API reference](https://developers.google.com/tasks/reference/rest/v1/tasks).
- Dependencies: BL-027. Rank 28 is in approved queue revision 15.
- Open questions: Which task fields may the skill set, and how should it handle missing dates or task lists?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-029 — Complete and remove Google Tasks
- Problem: a user cannot mark tasks complete or remove tasks through a repository skill.
- Intended outcome: mark tasks complete and delete selected tasks when asked.
- Scope: completion and deletion. Clearing all completed tasks is not included unless later approved.
- Evidence: user direction, 2026-11-17. Tasks API supports task updates, deletion and clearing completed tasks. [Tasks API reference](https://developers.google.com/tasks/reference/rest/v1/tasks).
- Dependencies: BL-027. Rank 29 is in approved queue revision 15.
- Open questions: Require exact confirmation before deleting a task? Should bulk clearing stay out of scope?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

### Google Contacts

#### BL-030 — Find and read Google Contacts
- Problem: the repository has no Contacts skill to find a user's contacts.
- Intended outcome: search and read personal contacts.
- Scope: personal contacts only. Search fields and displayed details remain open. Organization directory search stays out of scope.
- Evidence: user direction, 2026-11-17. People API supports listing and searching contacts. [People API contacts guide](https://developers.google.com/people/v1/contacts).
- Dependencies: none. Rank 30 is in approved queue revision 15.
- Open questions: Which search fields and contact details should the skill show?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-031 — Add and update Google Contacts
- Problem: a user cannot add or update a personal contact through a repository skill.
- Intended outcome: create a contact or change selected contact details.
- Scope: create and update personal contacts. Supported fields and duplicate handling remain open.
- Evidence: user direction, 2026-11-17. People API supports creating and updating personal contacts. [People API contacts guide](https://developers.google.com/people/v1/contacts).
- Dependencies: BL-030. Rank 31 is in approved queue revision 15.
- Open questions: Which contact fields may be changed? How should the skill identify a contact before an update?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

#### BL-032 — Delete Google Contacts
- Problem: a user cannot delete a personal contact through a repository skill.
- Intended outcome: delete a contact selected by the user.
- Scope: delete one identified personal contact. Bulk deletion and directory contacts are excluded.
- Evidence: user direction, 2026-11-17. People API provides a delete-contact method. [People API contacts guide](https://developers.google.com/people/v1/contacts).
- Dependencies: BL-030. Rank 32 is in approved queue revision 15.
- Open questions: What exact confirmation should be required before deletion?
- Status: Ready; stage requirements; backlog scope approved under approved queue revision 15. Requirements not approved.

- History: backlog revisions 68–69 recorded broad Gmail and Google service proposals. Revision 70 split them into BL-016–BL-032 in service order. The user approved backlog revision 70 on 2026-11-17, recorded as approved queue revision 15. Requirements approval remains separate.

Retired IDs: BL-002, BL-003, BL-004, BL-005, BL-006, BL-007, BL-008, BL-010, BL-011, BL-012, BL-013 and BL-014. Do not reuse these IDs. See the [archive](iterations/retired-backlog-items-revision-10.md).

### BL-015 — Expose database CRUD operations to the LLM

- Problem: database creation, configuration and table operations are not available through a clear set of callable Python tools; existing database use is embedded in import functions.
- Intended outcome: add functions to create or link an existing database, update its configuration, and perform create/read/update/delete operations for each of five tables. Refactor other functions to use these operations so an LLM can call them. The user selected one public function per table for each operation; architecture proposes shared private helpers. Scope revision 2 adds `transactions.user_comment` and a safe update for existing databases.
- Evidence: direct `/plan` request, 2026-11-10. `tools/database.py` is empty. `skills/banking-financial-history/scripts/bank_history.py` contains direct SQLite schema and query operations across five tables.
- Dependencies: BL-001. Rank 15 is a proposed placement after the existing ranked items. BL-015 was active in single mode before completion; approved queue revision 9 remains unchanged.
- Database link rule: inspect the five expected tables. If they are missing, ask whether to create the tables or use another database. User confirmed this on 2026-11-12.
- Settings rule: save the selected history directory in the existing financial-history settings file and preserve other settings. User approved a settings file on 2026-11-12.
- Python interface: use plain Python functions called by the financial-history skill's Python runner. Do not add LangChain or MCP wrappers in this feature. User selected this option on 2026-11-13.
- Scope revision 2: add a nullable `user_comment` field to `transactions`. Update only the transaction row and keep original statement evidence unchanged. On linking a compatible existing database, add only the missing column and preserve existing rows. This is the only schema update in this revision. Scope change approved as APR-DB-SCOPE-002 on 2026-11-13.
- Scope revision 3: delete dependent rows when database links require it; deleting a source statement record removes its child transaction, while deleting a transaction keeps its source record and clears its `transaction_id` link. Keep source evidence fields and files on disk. Requirements DBR-010–DBR-011 and architecture ADR-DB-010 remain approved as APR-DB-REQ-003 and APR-DB-ARCH-003.
- Scope revision 4: one shared Read function accepts an optional free-text expression after `WHERE`, selected columns, `GROUP BY`, and summaries. Without a `WHERE` expression, it uses all rows from the selected table. The filter applies only to the selected table, with separate bound values. Initial summaries are `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`. Read requirements DBR-012 were approved as APR-DB-REQ-004. Read requirements and architecture decisions from revision 3 are superseded; delete decisions remain unchanged.
- Scope revision 5: use one Read function per table and keep the scope revision 4 filter, values, selected columns, grouping, summaries, and safety rules. The table is fixed by each function name. Requirements DBR-013 were approved as APR-DB-REQ-005.
- Status: Done. The follow-up fix starts a write transaction before Create and Update validate linked rows. A concurrent check passed; the statement-upload tests passed (12 tests, 12 subtests); Python compilation and `git diff --check` passed. Code review, security review, and simplification review found no remaining issue in this change. Ruff was not available. No test files changed and no real financial history was used. BL-015 remains outside approved queue revision 9.

The nine retired item IDs and their approved scope text remain in the [queue revision 10 archive](iterations/retired-backlog-items-revision-10.md). Do not reuse these IDs.

### BL-001 — Persistent ingestion, account/card inventory and coverage

Current status: **Done for scope revision 9.** The user approved design revision 6 as APR-ING-DES-007 and revised step 4 as APR-ING-IT4-002. Implementation adds checked amount-format evidence and Excel workbook epoch handling, structured whole-statement errors, malformed format checks, and tracked tests. All five test files passed 157 tests and 166 subtests in the Coordinator's final run. Compilation and `git diff --check` passed. Ruff is unavailable. Independent code and security reviews passed after repairs. No real history was used and no install was performed.

### BL-001 history (historical checkpoints)

Lifecycle record: [bank ingestion lifecycle](iterations/bank-ingestion-lifecycle.md), [Product Owner requirements plan](iterations/bank-ingestion-requirements-product-owner-plan.md). Product Owner PLAN-BANK-001 r1 selected the highest ranked Ready unfinished item after the user asked `/plan next` on 2026-10-26. The statements below record earlier stages; later approvals and the completion record supersede their status.

Historical requirements checkpoint: [revision 3](iterations/bank-ingestion-requirements.md) was approved under APR-ING-REQ-003, including header-period cases, ING-010-A–J and defaults. Revisions 1/2 remain unapproved snapshots.

Historical architecture checkpoint: [revision 1 proposal](iterations/bank-ingestion-architecture.md), ARCH-D01–D06 plus dependency/security boundaries, returned by Architect ARCH-BANK-001 r1. Its pending approval status was later superseded by architecture revision 2 approval, design approval and implementation approvals.

Historical change, 3 November 2026: the user requested a header-date comparison before a repeat import. [Requirements revision 4](iterations/bank-ingestion-requirements.md) changed the standard import rule for fully covered periods and accepts new data only for uncovered periods. The user approved requirements revision 4, then architecture revision 2, design revision 3 and implementation steps 1–3. Current status appears above.

- Problem: PDF tables and bank exports vary; unverified extraction undermines all analysis.
- Intended outcome/scope: one reusable ingestion skill using existing `pdf`/`xlsx` capabilities for supplied text PDFs and CSV/XLSX from personal bank and credit-card accounts. Preserve source/page/row, raw description, account alias, dates, signed amount and currency, distinguishing unknown values. Flag extraction uncertainty, overlapping periods and reconciliation differences; identify unavailable balances rather than claiming reconciliation. Recognise scanned inputs as unsupported in this version. Keep currencies separate.
- Scope revision 2 extension (historical): persist reusable transaction history across sessions for savings, transaction and credit-card accounts; incrementally add statements. At this point, storage and source retention remained open. Later scope revision 8 selected local SQLite and retained original copies.
- Scope revision 3 supersedes monthly-input wording: accept any statement frequency and changes per account, including custom/ad hoc ranges. Track the union of verified coverage intervals separately from transaction dates. Overlaps add no extra coverage; uncertain or partial imports do not silently establish complete coverage. Infer and adapt cadence per account where evidence permits, but use it only for expectations, never as proof of coverage. Assess exact gaps within an agreed review horizon and account active dates; request the missing date range, not a particular count of files. Declared statement/export range or user confirmation supports boundaries; transaction min/max alone does not. Record covered, missing, partial/failed, uncertain and unavailable ranges distinctly. A confirmed no-activity period is not equivalent to an uploaded statement. The latest covered date is not necessarily today.
- Scope revision 4 confirms a durable inventory for each account and its date ranges, updated after each import/correction. Track coverage status and supporting sources; derive exact missing intervals within the review horizon. Expose this inventory to Banker and all analyses. User reference: immediate-analysis/account-inventory clarification, 2026-10-24.
- Scope revision 5: accept multiple files in one batch, across accounts and overlapping/different periods. Record each file's outcome: imported, already represented, partially imported, failed or unsupported, with reasons/source evidence. Successful files contribute to saved history/coverage even when others fail; failed or uncertain portions do not establish verified coverage. Immediately analyse usable data, label gaps and request only unresolved ranges. Reference: user batch-upload clarification, 2026-10-24; [batch/context discovery plan](iterations/banker-batch-context-discovery-product-owner-plan.md).
- Scope revision 6: distinguish accounts from linked cards/payment instruments. Preserve account balances, debt and coverage once even when several cards share the account. Link cards using statement evidence or user confirmation; matching masked digits alone does not establish identity. Keep original-file retention, persistence location and files/database choice open for later evaluation. Evaluate exact totals, correction integrity, import recovery, portability and retention; vectors are optional similarity retrieval and must not be the source for balances or coverage. Reference: latest user storage/consolidation decisions, 2026-10-24, and [tagging discovery plan](iterations/banker-tagging-discovery-product-owner-plan.md); E11/E12/E13.
- Scope revision 7: one shared authoritative history for ingestion, tagging and reporting scripts. Consider transactions/accounts/tagging mappings as core record groups, with linked cards, dated balance observations, import/source evidence and disjoint coverage intervals as supporting records. Preserve original descriptions and transaction/posting dates where supplied. Balance observations carry date, type and source; targets and required safety buffers remain distinct user settings. Maintain correction provenance and exact monetary values with explicit currency precision rather than binary floating-point totals. Files/SQLite/service database and optional vector retrieval remain candidates, not selected schema/architecture. Reference: user storage brainstorming, 2026-10-25, [storage discovery plan](iterations/banker-storage-discovery-product-owner-plan.md), E16–E19.
- Scope revision 8: use one local personal SQLite dataset as shared persistent history for ingestion, tagging, analysis and reporting. Retain original statement copies in a source folder alongside the database, preserving provenance. Start with generic text PDF and CSV/XLSX support, not restricted to named banks; ambiguous/unsupported layouts retain explicit import outcomes and coverage uncertainty. This supersedes earlier storage-candidate/source-retention uncertainty. Later requirements, architecture and design approvals defined implementation. Reference: user's final choices, 2026-10-26, [final proposal plan](iterations/banker-final-proposal-product-owner-plan.md).
- Scope revision 9: pass date patterns and amount separator/grouping values as strings on each record. Use Python date parsing/formatting and exact decimal conversion. If any date or amount format is invalid or conversion fails, stop that whole statement and raise a structured, actionable field error; do not save rows or coverage from that statement. Keep the existing source, sign and no-guess checks. Other import uncertainties retain the approved partial-import behavior. User requested string variables and whole-statement stop on 5 November 2026; design approval APR-ING-DES-006.
- Rationale/evidence: local PDF and XLSX skills already cover extraction/import; E1 and E3 support traceability and minimisation. Shared ingestion prevents divergent analysis totals.
- Design and implementation resolved data records, location, recovery and deletion behaviour. SQLite, source-copy retention and generic initial support are selected. No sample statements were supplied; tests use generated data, so support for real statement layouts remains unverified.
- Dependencies: none. Direct-request reference: user `/backlog`, 2026-10-24, and format/account discovery answers. Scope approval: APR-BANK-008 (2026-10-26).
- Lifecycle and completion records: [Product Owner plan](iterations/bank-statement-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-ingestion-step-3-coordinator-plan.md), [independent test plan](iterations/bank-ingestion-step-3-tester-plan.md), [code review](iterations/bank-ingestion-step-3-code-reviewer-plan.md) and [security review](iterations/bank-ingestion-step-3-security-reviewer-plan.md). Design revision 5 is approved as APR-ING-DES-006; implementation awaits a separate approval.

### BL-006 — Retired

- Current scope: use `banking-financial-history/SKILL.md` and the existing database Read functions for on-demand analysis and reports. Do not add a Python analysis engine or save analysis results, budgets, goals or report versions.
- Supported questions: duplicate and unusual entries; recurring payments; spending and cash flow; fees and interest; conditional forecasts; recurring price changes; and comparisons with goals or budgets the user supplies for that request.
- Output: give the selected executive summary and detailed report when requested. State the period, currencies, coverage gaps, evidence and assumptions. Keep uncertain or uncategorised rows visible. Create a report file only when requested, using an existing document skill.
- Limits: do not edit transactions, save classifications or transfer links, or promise alerts. The current skill reads one table at a time and does not page Read results. Category analysis needs saved tags; if tags are unavailable, report uncategorised activity.
- Scope revision 4 was approved as APR-BANK-REVIEW-001 on 2026-11-15. Earlier scope text is in the [queue revision 10 archive](iterations/retired-backlog-items-revision-10.md).
- On 2026-11-15, the user approved retiring BL-006 as a separate item and keeping the current financial-history skill. No requirements proposal or skill change is needed.
- On 2026-11-15, the user approved removing BL-006 as a dependency of BL-007 so it can use the existing financial-history skill. Queue revision 13 selects BL-007 at requirements.
- Scope revision 4 remains in the [retired item archive](iterations/retired-backlog-items-revision-10.md). Do not reuse BL-006.

### BL-007 — Retired

- Problem: users need one conversational guide to gather missing inputs, invoke repeatable analyses and explain what matters across accounts.
- Intended outcome/scope revision 1: add a distributed subagent named `banker`; it invokes ingestion/coverage and analysis/reporting skills, presents missing or uncertain date ranges, requests inputs that cover those ranges, and remembers supplied coverage. Adapt to each account's observed statement timing without requiring fixed periods or counts. Turn calculated summaries from one or more skills into a plain-language executive summary and prioritised suggested actions, with numerical claims traceable to results and source evidence.
- Scope revision 2: user confirms immediate available-data analysis with gaps labelled, rather than waiting for completeness or asking permission to proceed. Consult/update the durable account/date-range inventory; ask for missing ranges alongside results and refresh affected findings after new data arrives. Label affected comparisons and forecasts provisional or unavailable where evidence is insufficient; never invent missing transactions/balances. Present conditional shortfall warnings from the financial-history skill when its evidence supports them. User reference: immediate-analysis/account-inventory clarification and forecast request, 2026-10-24.
- Scope revision 3: Banker works in its own isolated working context. The main chat receives summary reports and the executive summary, including material warnings, data limitations and unresolved missing-range requests. Detailed transaction records, extraction outputs and processing logs remain in Banker's context or saved artifacts. Resume from durable inventory, history, corrections, findings and report records rather than previous chat context. Numeric claims remain traceable to saved results. Actual isolation/handoff must be verified later; this is not a demonstrated privacy boundary. Reference: user context-separation clarification, 2026-10-24; batch/context discovery plan linked under BL-001.
- Scope revision 4: invoke the dedicated tagging skill where needed, surface ambiguous tags/consolidation and missing buffer settings without withholding other findings. Executive synthesis covers supplied accounts collectively with account-specific risks and evidence-supported card breakdowns. Selected summary+detailed report output supersedes workbook-related uncertainty. Reference: latest user tagging/report/consolidation decisions, 2026-10-24; tagging discovery plan under BL-001.
- Boundaries: separate facts, uncertain interpretations and optional actions. Suggested checks may concern an unfamiliar charge, recurring price change or missing data. Sending messages, disputing charges, cancelling services and moving money remain outside scope. No autonomous financial actions or schedules proposed.
- Rationale/evidence: direct user Banker brainstorming and variable-frequency/range-coverage clarification, 2026-10-24. Existing agent definitions and skill Python helpers establish repository conventions, not implemented financial capability.
- On 2026-11-15, the user decided the separate Banker feature was not required and approved closing the requirements proposal. The current financial-history skill already checks periods and gaps, reports limits, and gives an after-import health check.
- No subagent, separate context, new skill instructions, application, or code is planned. Do not reuse BL-007.
- Scope revisions 1–4 remain in the [retired item archive](iterations/retired-backlog-items-revision-10.md).
- Lifecycle records: [Banker Product Owner plan](iterations/banker-discovery-product-owner-plan.md), [Coordinator plan](iterations/bank-statement-discovery-coordinator-plan.md). Completion evidence: none.

### BL-009 — Transaction tagging and merchant identification skill

- Current status: **Done.** User approved removing the database version marker because new installs create a fresh database. See the [BL-009 lifecycle](iterations/bank-tagging-lifecycle.md).
- The implementation uses `skills/banking-financial-history/scripts/bank_history.py`. New histories include the tagging schema. Setup asks before it adds missing tables or fields to a linked history.
- Focused tests pass: 25 tests and 12 subtests. Compilation and diff checks pass. Main-chat code, security and simplification reviews pass. These reviews are not independent. Ruff is not installed.
- No saved history was opened or changed. The skill was not installed. No further BL-009 action is active.

### BL-010 — Retired

- On 2026-11-15, the user decided the feature had no separate value because the LLM can already answer financial questions from the saved SQLite data. The user approved retiring BL-010 and removing it as a BL-006 dependency.
- Keep the existing account, currency, transfer and card-payment guidance in `banking-financial-history/SKILL.md`. Do not add dedicated code, schema, or saved transfer links for this item.
- Scope revisions 1 and 2 remain in the [retired item archive](iterations/retired-backlog-items-revision-10.md). Do not reuse BL-010.

## Storage and workbook distinction

Storage remains open: evaluate authoritative structured history in files or a database for exact calculations, stable identity, corrections, recovery and portability; retain source/report files according to chosen retention policy. Optional vector retrieval may help find similar descriptions/explanations, but must not determine balances, coverage or exact transaction identity from approximate matches. E11 and E12 support these different purposes, not a choice of technology. No database, vector service or embedding transfer approved.

**Historical discussion above and below is superseded by the 2026-10-26 choice:** SQLite is selected for one local personal dataset, source copies retained alongside it. Vectors remain unselected. The candidate comparison is retained as decision history; it is not an unresolved engine choice. Detailed schema/design and runtime/data-security verification remain later-stage work.

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

## Discovery closure and later-stage details

Historical discovery record: the user selected local SQLite, retained source copies, all 14 items and generic initial bank support, then approved revision 8 under APR-BANK-008. Queue revision 14 supersedes the 14-item queue: twelve items are retired and BL-009 is Blocked pending implementation reconciliation. Requirements, design and implementation approvals remain separate.

Later-stage details: exact data contracts/schema and recovery/deletion behaviour; detailed-report format and representative generic-format examples; tagging taxonomy/review thresholds and account/card/transfer evidence rules. During use, users supply actual account safety buffers, savings targets and budgets. No named-bank compatibility or extraction accuracy claim exists before validation. Vectors are not part of the selected baseline.

Resolved: immediate analysis/gap labels; persistent account/range inventory; batch uploads; Banker own context/main-chat summaries; adjustable 30-day forecast; required user-set per-account buffers; summary+detailed report, no required workbook; separate tagging skill; consolidated accounts/cards/transfers; extras separately tracked. Do not re-ask these decisions.

## Revision and decision history

- 2026-11-10 — Revision 15 adds BL-015 from the direct `/plan` request. Rank 15 is proposed after the existing items; approved queue revision 9, ranks 1–14 and active selection remain unchanged. `tools/database.py` is empty; `bank_history.py` performs direct SQLite operations. No code changed.
- 2026-11-10 — User approved BL-015 scope revision 1 and selected one Create function per table. Coordinator marked BL-015 Ready at requirements without changing rank or approved queue revision 9. Other CRUD function shapes and database linking rules remain open. No requirements, design or implementation approval is recorded.
- 2026-11-12 — User confirmed that linking a database checks for all five expected tables and asks whether to create the tables or use another database if they are missing. Requirements discovery found that no saved database path setting exists in the current script. Config storage and update behaviour remain open. No code changed.
- 2026-11-12 — User approved saving the selected history in a settings file. Coordinator selected single-item mode for the directly requested BL-015 work, without changing approved queue revision 9 or ranks 1–14. Requirements proposal saved at [database CRUD lifecycle](iterations/database-crud-lifecycle.md); it awaits approval. No code changed.
- 2026-11-13 — User selected setup option A (ask whether to create only missing tables or use another database), update/delete option A (a clear direct request is enough), and Python interface option A (plain functions called by the skill's Python runner). Requirements proposal updated; it still awaits approval. No code changed.
- 2026-11-13 — User approved requirements DBR-001–DBR-007 as APR-DB-REQ-001. BL-015 advances to architecture in single-item mode. Approved queue revision 9 and ranks 1–14 remain unchanged. No code changed.
- 2026-11-13 — User selected per-table functions for Read, Update, and Delete. Coordinator saved architecture ADR-DB-001–ADR-DB-005, recommending per-table public functions with shared private helpers. BL-015 awaits architecture approval; requirements remain approved and unchanged. No code changed.
- 2026-11-13 — User approved architecture ADR-DB-001–ADR-DB-005 as APR-DB-ARCH-001. BL-015 advances to solution design in single-item mode. The queue and ranks remain unchanged. No code changed.
- 2026-11-13 — User selected updating only the transaction row while retaining the original source record, and asked to add a “changed by user” comment. The current schema has no comment field and the approved architecture excludes schema changes. Design pauses for a scope decision. No approval or evidence is invalidated yet; no code changed.
- 2026-11-13 — User approved scope revision 2 as APR-DB-SCOPE-002: add `transactions.user_comment` and safely add this column to existing histories. Requirements revision 2 is proposed as DBR-008–DBR-009 and awaits approval. Requirements and architecture approvals for scope revision 1 remain historical; architecture revision 2 is needed after requirements approval. No code changed.
- 2026-11-13 — User approved DBR-008–DBR-009 as APR-DB-REQ-002. BL-015 advances to architecture revision 2. Architecture revision 1 remains historical for scope revision 1. No code changed.
- 2026-11-13 — Coordinator saved architecture revision 2 with a one-column additive update, transaction comment handling, and explicit insert columns for imports. ADR-DB-006–ADR-DB-009 await approval as APR-DB-ARCH-002. No code changed.
- 2026-11-13 — User approved architecture ADR-DB-006–ADR-DB-009 as APR-DB-ARCH-002. BL-015 advances to solution design. No code changed.
- 2026-11-13 — User chose Read option B, all matching rows. Coordinator saved solution design SD-DB-001–SD-DB-006, including table contracts, setup flow, comment handling, and existing-database update. Design awaits approval as APR-DB-DES-001. No code changed.
- 2026-11-13 — User requested cascading deletion of related rows and SQL queries for Read. These changes require scope revision 3. The affected rows and SQL function interface need clarification before requirements work. Requirements and architecture approvals for revision 2 remain historical; no code changed.
- 2026-11-13 — User clarified scope revision 3: delete dependent rows when a database link requires it, and keep the source record when deleting a transaction unless required. User chose one shared Read function with a table name and search clause. Coordinator saved DBR-010–DBR-011 as a requirements proposal. Awaiting approval; no code changed.
- 2026-11-13 — User approved requirements DBR-010–DBR-011 as APR-DB-REQ-003. BL-015 advances to architecture revision 3. Coordinator asks the user to choose between schema-level cascade rules and child-first delete operations before completing the architecture proposal. No code changed.
- 2026-11-13 — User chose child-first Python deletion in one transaction. The schema stays unchanged for this behavior. Search-clause format remains open before architecture analysis is complete. No code changed.
- 2026-11-13 — User chose a SQL-style search clause with separate values. Coordinator saved architecture revision 3, ADR-DB-010–ADR-DB-012, comparing delete and Read alternatives and defining a checked clause boundary. It awaits approval as APR-DB-ARCH-003. No code changed.
- 2026-11-13 — User approved architecture ADR-DB-010–ADR-DB-012 as APR-DB-ARCH-003. BL-015 advances to solution-design discovery. Coordinator asks for the supported search syntax before completing the design. No code changed.
- 2026-11-13 — User requested a free-text `WHERE` expression, `GROUP BY`, and selected columns for Read. User clarified that filters apply only to the selected table and that summaries are needed. Coordinator proposed DBR-012 with bound values and `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`. It awaits requirements approval. Delete requirements and ADR-DB-010 remain approved; Read decisions from revisions 3 are superseded. No code changed.
- 2026-11-13 — User clarified that the `WHERE` expression is optional. Coordinator updated DBR-012: an absent or empty expression uses all rows before grouping or summaries. Requirements approval remains pending. No code changed.
- 2026-11-13 — User approved DBR-012 as APR-DB-REQ-004. BL-015 advances to architecture revision 4 for the Read behavior. Need decide how to check free-text filtering and how callers express summary functions. No code changed.
- 2026-11-13 — User chose SQLite access controls for the free-text `WHERE` expression and summary expressions inside `selected_columns`. Coordinator saved architecture ADR-DB-013–ADR-DB-015, with read-only access, selected-table restrictions, grouped-result rules, and comparison of a custom parser. It awaits approval as APR-DB-ARCH-004. No code changed.
- 2026-11-13 — User approved architecture ADR-DB-013–ADR-DB-015 as APR-DB-ARCH-004. BL-015 advances to solution design revision 4. Coordinator read `bank_history.py`, the financial-history skill, and relevant ingestion test callers to reconcile the design. No code changed.
- 2026-11-13 — Coordinator saved solution design SD-DB-007–SD-DB-012 covering setup, config, per-table Create/Update/Delete, shared Read, cascades, import refactoring, and skill use. It awaits approval as APR-DB-DES-004. No code changed and no tests ran.
- 2026-11-14 — User requested separate Read functions for each table. Coordinator recorded scope revision 5 and proposed DBR-013. It keeps scope revision 4 Read behavior while removing the table-name input. Requirements await approval; no code changed.
- 2026-11-14 — User approved DBR-013 as APR-DB-REQ-005. BL-015 advances to architecture revision 5. Coordinator recommends fixed-table public wrappers over one shared private query helper. No code changed.
- 2026-11-14 — Coordinator saved architecture ADR-DB-016–ADR-DB-017, comparing per-table duplicated queries with fixed wrappers over one safe helper. The proposal awaits approval as APR-DB-ARCH-005. No code changed.
- 2026-11-14 — User approved architecture ADR-DB-016–ADR-DB-017 as APR-DB-ARCH-005. BL-015 advances to solution design revision 5. No code changed.
- 2026-11-14 — Coordinator saved solution design revision 5 with per-table Read functions over one private query helper. It carries forward the approved setup, CRUD, deletion, and import contracts and updates the skill mapping. The design awaits approval as APR-DB-DES-005. No code changed and no tests ran.
- 2026-11-14 — User approved solution design revision 5 as APR-DB-DES-005. Coordinator saved iteration plan DB-IT-001 for two coding steps in `bank_history.py` and `SKILL.md`. The plan awaits approval as APR-DB-IT-001. No code changed and no tests ran.
- 2026-11-14 — User approved iteration plan DB-IT-001 as APR-DB-IT-001. Coordinator prepared coding plan APR-DB-CODE-001 for the two approved source files. Coding awaits approval; no code changed and no tests ran.

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
- 2026-10-26 — Revision 8 final discovery proposal: user chose `1A, 2A, 3A, generic initially`: one local personal SQLite dataset, retained originals alongside database, all 14 separately prioritised items and generic initial bank support. Product Owner DISC-BANK-009 r1 reconciled direct decisions; Coordinator advanced only BL-001 to scope revision 8, retained other scopes/ranks/dependencies and archived exact r7. No new research/design/schema/implementation performed. No discovery blockers remain.
- 2026-10-26 — **APR-BANK-008:** user replied **“yes approved”** to the exact revision 8/all-14 approval request. Coordinator recorded approval, marked BL-001–BL-014 Ready without scope/rank/dependency changes, and closed discovery. Approval applies to each current item scope revision in the table and supersedes all earlier pending-approval wording. No active item or execution queue selected; no requirements/design/implementation approval or feature completion inferred.
- 2026-10-26 — User `/plan next`: Product Owner PLAN-BANK-001 r1 verified BL-001 scope8/rank1 eligible (Ready, no dependencies, no active item). Coordinator recorded queue mode/approved queue revision8, active BL-001 In Progress at requirements, and lifecycle links before requirements continuation. No scope/rank changes or downstream approval.
- 2026-10-26 — Product Owner PLAN-BANK-001 r1 returned requirements revision1 ING-001–ING-014, including explicit defaults; Coordinator persisted complete coverage and the ING-012 deletion-intent refinement. BL-001 Awaiting Approval at requirements; all other items remain Ready. No feature scope/rank changes, requirements approval, design or implementation.
- 2026-10-26 — User requested repeated-monthly and yearly-over-month import logic. Product Owner PLAN-BANK-001 r2 refined ING-010 only with separate file/transaction matching, provenance, multiplicity, ambiguity and interrupted retry, plus ten acceptance cases. Coordinator preserved requirements r1 and saved r2; BL-001 still Awaiting Approval at requirements, queue8 active. No backlog scope/rank changes or downstream approval.

- 2026-10-26 — User clarified statement coverage comes only from header periods or explicit user answer, never transaction dates/inactivity. Product Owner PLAN-BANK-001 r3 refined ING-007/008; Coordinator saved requirements r3 and preserved r2. BL-001 remains Awaiting Approval at requirements, queue8 active; no approved backlog scope/rank changes.

- 2026-10-26 — APR-ING-REQ-003: user approved requirements revision3. Coordinator recorded approval without changing criteria, set BL-001 In Progress/architecture and continued queue8 at the next applicable stage. Architecture/design/iteration/implementation remain unapproved.
- 2026-10-26 — Architect ARCH-BANK-001 r1 returned architecture revision1, six decisions/alternatives, Mermaid, dependency/security boundaries and complete ING coverage. Coordinator saved/reconciled proposal and XLSX fail-closed/dataflow clarifications; BL-001 Awaiting Approval at architecture, queue8 active. No scope/rank changes, solution design, code or runtime tests.
- 3 November 2026 — User requests header-date checks against prior coverage before repeat imports. Product Owner PLAN-BANK-001 r4 changes ING-007/009/010. Coordinator keeps approved requirements 3, saves proposed requirements 4 and returns BL-001 to requirements approval. Architecture 1 needs an update after approval. Backlog scope, ranks and queue 8 stay unchanged. No code changed.

- 3 November 2026 — APR-ING-REQ-004: the user approved requirements revision 4. The Coordinator recorded approval and set BL-001 In Progress at architecture. Queue 8, scopes and ranks stay unchanged. The Architect must update the plan before architecture approval. No code changed.
- 3 November 2026 — Architect ARCH-BANK-001 r2 returned architecture revision 2. Decisions D03–D05 and the diagram now use the approved date-range check. The Coordinator saved the proposal and kept the previous version. BL-001 awaits architecture approval. The other 13 items stay Ready. No code changed.

- 3 November 2026 — APR-ING-ARCH-002: the user approved architecture revision 2. The Coordinator recorded approval and set BL-001 In Progress at solution/UI design. The next work defines tables, script commands and failure handling. No new screen or code. Queue 8 stays active.

- 3 November 2026 — Solution designer DESIGN-BANK-001 r1 returned the detailed design. The Coordinator saved records, commands, exact amounts, range checks, recovery, deletion and review corrections. BL-001 awaits detailed design revision 1 approval. All other 13 items stay Ready. No code or tests.

3 November 2026 — simplified design checkpoint: [detailed design revision 2](iterations/bank-ingestion-solution.md) replaces the unapproved first proposal with eight tables, five main commands and two Python files. Requirements 4 and architecture 2 remain approved and unchanged. BL-001 awaits design approval. Queue revision 8, ranks, scopes and other item states remain unchanged. No implementation approval.

Design clarification checkpoint: [revision 3](iterations/bank-ingestion-solution.md) separates original statement records from accepted transaction values and defines Python function inputs/results plus four import examples. The user authorised clarification work, not design or development. BL-001 awaits design revision 3 approval; approved requirements, architecture, queue and other item states remain unchanged.

### 4 November 2026 — step 3 approval

The user asked to “continue with step 3 development”. This approves the saved step 3 scope under APR-ING-IT3-001. Step 3 covers corrections, recovery, export/restore/deletion, skill instructions and catalogue updates, with checks for ING-001–014. The existing `bank_history.py` includes unreviewed step 3 work; the current combined source must pass tests and independent reviews before BL-001 can advance. The step 2 frozen hash and its tests/reviews remain historical evidence only.

### 4 November 2026 — BL-001 complete

Step 3 implementation passed independent testing, code review and security review. TEST-BANK-003 r4 reports 122 tests and 69 subtests passed; compilation passed. REVIEW-BANK-003 r4 passed. SEC-BANK-003 r2.1 passed after the Coordinator corrected the earlier security record and reconciled the current records. Source/test inventory and limits are in the step 3 specialist plans. BL-001 is Done. The approved queue revision and all other item ranks/scopes remain unchanged. No next item is active.

### 4 November 2026 — queue resumed at BL-009

The user invoked `/next`. Product Owner PLAN-QUEUE-001 r1 selected BL-009 scope revision 2, rank 2. It is Ready under approved queue revision 8 and depends only on BL-001, which is Done. Coordinator resumed the existing queue request and set BL-009 In Progress at requirements. No scope or rank changed. `/next` does not approve requirements; design remains blocked until explicit requirements approval. See [queue resume record](iterations/bank-queue-resume-coordinator-plan.md) and [BL-009 lifecycle](iterations/bank-tagging-lifecycle.md).

### 5 November 2026 — BL-009 implementation complete

The user approved step 2 and local storage without encryption. The Developer completed the tagging functions, skill and catalog updates, including safe bounded paging and rule reads. Focused tests and all independent reviews passed. The full ingestion suite had 12 XLSX failures because `defusedxml==0.7.1` is missing; no package was installed. Ruff was unavailable. No real history was opened or changed, and no skill was installed. Coordinator marked BL-009 Done and left the next queue item unselected. See [step 2 completion](iterations/bank-tagging-iterations.md#step-2-completion--5-november-2026).

### 5 November 2026 — BL-001 format design revision 5 approved

The user approved design revision 5 as APR-ING-DES-006. Scope revision 9 replaces fixed format keys with string date patterns and amount separator/grouping values. The user selected whole-statement failure when any date or amount format fails. Source checks, exact money and the history schema remain unchanged. The Coordinator saved an implementation plan. BL-001 is Awaiting Approval at implementation planning; no code changed. Queue revision 9 keeps all ranks and other scopes unchanged. No next item is selected.

The Product Owner saved [requirements revision 1](iterations/bank-tagging-requirements.md), with TAG-001–TAG-010 and proposed defaults. Coordinator set BL-009 to Awaiting Approval at requirements. No design or implementation approval is inferred. The user must approve or revise the exact requirements proposal before the next stage.

The user replied “approved” to BL-009 requirements revision 1. Coordinator recorded APR-ING-REQ-005 without changing the text and advanced BL-009 to architecture. Architecture, design and implementation remain separate approval stages.

The user replied “approved” to BL-009 architecture revision 1, option A. Coordinator recorded APR-ING-ARCH-003 without changing it and advanced BL-009 to solution design. Implementation remains unapproved.

Solution Designer DESIGN-BANK-009 r1 first proposed two tagging tables. After the user asked why a separate tag table was needed, DESIGN-BANK-009 r2 moved current tags to transaction rows and kept one table for reusable rules. The user then asked to remove tag change history and approved that design update. DESIGN-BANK-009 r3 removes tag change history. The format 2 update still changes the completed BL-001 design. Coordinator saved [solution design revision 4](iterations/bank-tagging-solution.md). The user approved solution design revision 3 as APR-ING-DES-004. The Coordinator then found that approved requirements revision 1 says to keep tag changes. Revision 2 removes that conflict while preserving revision 1. The user approved revision 2 as APR-ING-REQ-006. Coordinator saved implementation steps revision 1. The user then directed that the history update use one database transaction and no separate copy. Coordinator saved solution design revision 4 and [implementation steps revision 2](iterations/bank-tagging-iterations.md). The user approved design revision 4 as APR-ING-DES-005 and step 1 as APR-TAG-IT1-001. The Developer completed the approved step across six files. The independent Tester passed 97 focused tests and 70 subtests and compile checks. The wider ingestion suite had 12 failures because `defusedxml` is absent; no dependency was installed. Code and security reviews passed for the current files. No real history was opened or changed. The user accepted local storage without encryption for the initial version as APR-TAG-STORE-001. Step 2 is approved as APR-TAG-IT2-001 and is in progress. It does not permit installation or use on a saved history.

- 2026-11-15 — User approved coding as APR-DB-CODE-001. Coordinator implemented CRUD, setup/config, safe per-table Read functions, and import refactoring in the two approved files. `git diff --check` passed. No tests were added or run; checks await separate approval.

- 2026-11-15 — User approved the testing stage. Temporary SQLite checks passed for setup choices, legacy schema migration, CRUD, Read safety and summaries, linked deletes, and imports. `pytest -q tests/bank_statement_ingestion/test_statement_upload.py` passed 12 tests and 12 subtests. `git diff --check` passed. No real financial data or test-file changes. Code review awaits approval.
- 2026-11-15 — User approved the code-review stage. Review of `bank_history.py` and `SKILL.md` found a concurrency defect: Create and Update validate links before they start a write transaction. Concurrent calls can pass the same validation and save conflicting links. Python 3.14 documentation confirms that, with the default legacy transaction mode, SQLite does not open a transaction for SELECT; it opens one before DML. The recommended fix is to start `BEGIN IMMEDIATE` before validation in the public Create and Update paths. Review did not edit source. Await user approval for this remediation. Existing checks remain evidence for the reviewed version only.
- 2026-11-15 — User approved the remediation and required checks. A temporary-data reproduction confirmed the defect: two concurrent Create calls both saved a transaction for one source row. `bank_history.py` now starts `BEGIN IMMEDIATE` before validation in Create and Update. A concurrent Create/Update check passed and confirmed that the account and linked transaction remain consistent. `pytest -q tests/bank_statement_ingestion/test_statement_upload.py` passed 12 tests and 12 subtests; `python3 -m compileall -q skills/banking-financial-history/scripts/bank_history.py` and `git diff --check` passed. Ruff was unavailable. Follow-up code, security, and simplification reviews found no remaining issue in the fix. No tests or real financial data changed. BL-015 is Done.
- 2026-11-15 — User approved switching to queue mode and starting BL-010. BL-010 is the highest-ranked Ready item with completed dependencies (rank 3; BL-001 is Done). Coordinator set BL-010 scope revision 1 In Progress at requirements. Approved queue revision 9, ranks, dependencies and scope remain unchanged. Discovery scope remains approved under APR-BANK-008; requirements are not approved. See [BL-010 lifecycle](iterations/bl-010-account-consolidation-lifecycle.md).
- 2026-11-15 — **APR-BANK-REVIEW-001:** User approved a critical backlog review after testing the financial-history skill against saved SQLite data. Queue revision 10 retired nine separate analysis features and kept on-demand analysis in the skill workflow. BL-006 became skill-only, without custom analysis code or saved report history. BL-007 remains for runtime isolation and handoff. BL-009 is Blocked because this checkout lacks the implementation named in its lifecycle record and its current tagging skill says tagging is not ready. Prior ranks stay unchanged. The [archive](iterations/retired-backlog-items-revision-10.md) and [BL-010 lifecycle](iterations/bl-010-account-consolidation-lifecycle.md) record the review. No skill or Python source changed.
- 2026-11-15 — User said BL-010 had no separate value. The user approved retiring it and removing it as a BL-006 dependency. Queue revision 11 retained prior ranks and kept existing account and transfer guidance in the financial-history skill. See [BL-010 lifecycle](iterations/bl-010-account-consolidation-lifecycle.md). No skill or Python source changed.
- 2026-11-15 — User approved retiring BL-006 as a separate item and keeping the current financial-history skill. Queue revision 12 retains prior ranks. See [BL-006 lifecycle](iterations/bl-006-analysis-lifecycle.md). No skill or Python source changed.
- 2026-11-15 — User approved removing BL-006 as a dependency of BL-007 so BL-007 could use the existing financial-history skill. Queue revision 13 retained prior ranks. See [BL-007 lifecycle](iterations/bl-007-banker-lifecycle.md). No skill or Python source changed.
- 2026-11-15 — The user suggested adding any needed Banker guidance to the existing financial-history skill instead of building a separate agent. Coordinator prepared requirements proposal BKR-REQ-001, scope revision 5: rename BL-007 to Financial-history gap review and next-step guidance, report exact gaps within requested periods, and give evidence-based next checks. The user later said BL-007 had no separate value and approved retiring it and closing BKR-REQ-001. Queue revision 14 retains prior ranks. The current financial-history skill remains unchanged. No skill or Python source changed.
- 2026-11-15 — User approved BL-009 implementation and the design update that removes the database version number. Added tagging fields, `tagging_rules`, approved tag read/save functions, setup checks, user-approved missing-schema updates, and rule-aware account deletion to the current `financial-history` files. Added generated-data tests and updated the tagging skill, catalog, lifecycle and solution records. Focused tests passed (24 tests and 12 subtests); compile and diff checks passed. Main-chat code, security and simplification reviews passed; they were not independent. No real history was opened or changed, and the skill was not installed.
- 2026-11-15 — Follow-up check added `tag_reason` for TAG-005, database link and integrity checks for linked-schema updates, and a rule that web pages are evidence, not instructions. Final checks passed: 25 tests, 12 subtests, compile and diff checks. Main-chat code, security and simplification reviews passed again; they were not independent. BL-009 is Done. No real history was opened or changed, and the skill was not installed.
- 2026-11-15 — Direct `/plan` request to continue the email skill did not match an existing backlog item. Added BL-016 as Proposed outside approved queue revision 14. The current Gmail capabilities were recorded; the next capability remains to be defined. No Gmail code changed.
