# Bank ingestion requirements — Product Owner plan

Assignment PLAN-BANK-001 r1; 2026-10-26. Input: user `/plan next`, interpreted as next approved backlog item. Backlog r8/APR-BANK-008 supplied; independently verify selection. Initial stage queue selection; candidate BL-001 scope r8 unverified. No requirements until selected-state persistence acknowledgment.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| N1 | Approved backlog/active state | Verify highest-ranked eligible unfinished item | Done | Product Owner independently verified r8/APR-BANK-008, BL-001 r8 rank1 Ready/no deps, no active item | Coordinator persisted queue selection |
| N2 | Selected scope and repo evidence | Inspect complete scope after selection acknowledgment | Done | Product Owner read selected scope, PDF/XLSX capability evidence and actual pyproject >=3.13 | No application/scripts run |
| N3 | Requirements/criteria | Define bounded scope and observable success/failure cases | Done | ING-001–ING-014 cover complete scope; explicit proposed operational defaults | Requirements approval pending |
| N4 | Handoff | Return proposal and complete coverage checkpoint | Done | Full proposed requirements saved by Coordinator in bank-ingestion-requirements.md | Coordinator coverage reconciliation |

Initial checkpoint persisted. Specialist performs no edits, delegation, design or implementation. Requirements/design/iteration approvals remain separate. No approved inputs inferred from research or specialist output.

Selection checkpoint persisted: BL-001 scope8 active In Progress/requirements, execution mode queue, approved queue revision8/APR-BANK-008. N1 complete; N2–N4 pending. Coordinator acknowledges selected-state persistence before requirements batch. No other items advanced.

Final checkpoint persisted: N1–N4 complete. Product Owner maps every approved BL-001 scope paragraph to ING-001–ING-014; requirements revision1 proposed, no new feature scope. Proposed status Awaiting Approval after Coordinator final coverage check/presentation. No edits by specialist, no architecture/solution/iteration/implementation or tests. Generic inputs and synthetic verification scope avoid requiring private statements. Historical pending task statements above reflect prior checkpoints.

Pre-presentation refinement checkpoint persisted: Product Owner confirmed ING-012 recovery snapshots offered with disclosed scope/location/retention, user may decline or delete managed backups; no copy silently retained against deletion intent. Same proposed requirements revision1; other requirements unchanged. Coordinator checked full scope coverage/evidence links and saved BL-001 Awaiting Approval, queue8 active. No required checklist task remains; next explicit requirements approval only.

## PLAN-BANK-001 r2 — repeat/overlap refinement

User asks how repeated monthly and overlapping yearly imports avoid duplicate transactions. Requirements revision1 remains unapproved. Preserve backlog BL-001 scope8 and queue8; narrow requirements refinement only.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| D1 | ING-009/010/011 and approval state | Inspect repeat/overlap and correction requirements | Done | Product Owner inspected current pending proposal | — |
| D2 | Deduplication behaviour | Separate file repeat, record overlap, multiplicity and uncertainty | Done | Primary hashlib/SQLite evidence; file-vs-observation, one-to-one multiplicity and uncertainty rules returned | No design/runtime claim |
| D3 | Requirements revision2 | Return exact narrow wording and criteria/checkpoint | Done | Coordinator saved replacement ING-010 and A–J, preserving r1 | Requirements revision2 approval pending |

Initial r2 checkpoint persisted before continuation. No schema/SQL contract, tests, code or design approval. Feature remains Awaiting Approval at requirements.

Final r2 checkpoint persisted: D1–D3 done; coverage reconciled for repeated bytes/renamed files, changed same-name file, month/year overlap both orders, repeated legitimate purchases, reference conflicts, state/correction changes, covered-period unseen rows and interrupted retries. Only ING-010 changed; all other requirements/defaults unchanged. Backlog BL-001 scope8/rank1, queue8 and other13 Ready preserved. Requirements revision2 unapproved; next explicit approval of that revision.

## PLAN-BANK-001 r3 — header-only statement period

User directly clarifies: coverage start/end from statement headers only; missing/ambiguous dates require user answer, never transaction-derived boundaries. Requirements revision2 remains unapproved.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| H1 | ING-007/008 | Inspect current coverage and gap semantics | Done | Product Owner inspected pending r2 | — |
| H2 | Requirements r3 | Return header-only/user-answer wording and focused cases | Done | ING-007 replacement with eight cases, ING-008 unknown-vs-gap clarification | No other requirement changes |
| H3 | Handoff | Return scope/coverage checkpoint | Done | Coordinator persisted requirements r3 and preserved r2 | Requirements approval pending |

Initial checkpoint persisted. No new research/design/code; all other requirements, especially ING-010, preserved. Dataset facts remain immediately usable while coverage awaits user confirmation.

Final r3 checkpoint persisted: H1–H3 complete; eight cases cover empty periods, inactive edges, one/both missing boundaries, ambiguity, custom exports and user provenance. Only ING-007/008 changed; BL-001 scope8/rank1 and queue8 unchanged. No code/design/research/tests. Requirements r3 remains proposed; next approval supersedes r2 target.

Approval checkpoint, 2026-10-26: user explicitly approved requirements revision3; APR-ING-REQ-003 covers ING-001–ING-014, header-period cases, ING-010-A–J and defaults unchanged. Earlier pending/proposed references are historical. BL-001 advanced to architecture, queue8 retained; Architect separately assigned. No implementation/design approval inferred.

## PLAN-BANK-001 r4 — check saved date ranges first

3 November 2026. The user asks the skill to compare header dates with saved date ranges before loading the same period again. Requirements revision 3 remains the approved version. This request changes its rule to inspect every covered period. The proposed change needs requirements approval before further design.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| R1 | Approved requirements 3 | Read the rules that the request changes | Done | Product Owner read ING-007–011 | Approved copy saved |
| R2 | Proposed requirements 4 | Specify date checks and test cases | Done | Changes to ING-007/009/010 and cases A–N | Approval needed |
| R3 | Change record | Explain changed behaviour and effect on design | Done | Fully covered periods now stop standard import; architecture needs an update | Coordinator saved proposal |

The Coordinator saved this initial plan. No new research, code or design work. Keep retries and explicit corrections available. Use simple language.

Final record: R1–R3 complete. The Coordinator saved proposed requirements 4 and kept approved requirements 3. The change covers full and partial overlap, account/card limits, same-upload checks, retries, unclear headers and explicit corrections. No new research or code. BL-001 awaits requirements approval. The earlier architecture proposal cannot advance until the requirements and related design changes receive approval.

3 November 2026: the user approved requirements revision 4. Approval APR-ING-REQ-004 includes cases A–N and defaults. The Coordinator recorded approval without changing the requirements. BL-001 now continues at architecture. Earlier pending states remain historical records.
