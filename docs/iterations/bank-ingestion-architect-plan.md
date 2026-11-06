# Bank ingestion architecture — Architect plan

Assignment ARCH-BANK-001 r1; 2026-10-26; BL-001 scope8, backlog8/queue8 active. Approved input: requirements revision3/APR-ING-REQ-003. Stage architecture; feature In Progress. No architecture/solution/iteration/implementation approval.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| ARCH-001 | Approved scope and actual constraints | Reconcile requirements/backlog/lifecycle/repo | Done | Architect reconciled r3/APR-ING-REQ-003, backlog8/scope8/active architecture and historical lifecycle targets | No prerequisite conflicts |
| ARCH-002 | Existing extraction/distribution/dependencies | Inspect reuse and dependency boundaries | Done | Actual pyproject >=3.13/root only feedparser; PDF/XLSX extraction guidance and helper inventory inspected; no bank runtime; dependency absence explicit | Avoid recalc/save/vendoring |
| ARCH-003 | Alternatives and failures | Compare material ingestion/persistence/matching/recovery alternatives | Done | Six material alternatives and approved-requirement traces; official technical sources inspected | No runtime trials |
| ARCH-004 | Architecture proposal | Return decisions, Mermaid, dependency needs and approval target | Done | Architecture revision1/ARCH-D01–D06 returned and persisted by Coordinator | Architecture approval pending |
| ARCH-005 | Coverage/handoff | Reconcile ING-001–014 and ING-010-A–J, risks and limits | Done | Coverage table reconciles all requirements; recovery/identity/limits/dependency assumptions explicit | Coordinator final reconciliation |

Initial checkpoint persisted before substantive analysis. Architect read AGENTS.md, own role, planning/architecture skills. Fixed decisions: local SQLite, retained originals, header/user coverage, no implicit code/schema/API. No direct writes, Git, implementation or delegation by specialist. Next: ARCH-001/002 evidence batch, then checkpoint before alternatives continuation.

Evidence checkpoint persisted: ARCH-001/002 done; remaining ARCH-003–005 pending. PDF guidance uses pypdf/pdfplumber; XLSX openpyxl/pandas capabilities but its recalculation script rewrites workbooks and markitdown loses coordinate provenance. Reuse installed extraction guidance/read-only libraries; do not assume dependencies, workbook deliverables or recalc. Existing skill frontmatter licenses are Proprietary: no copied/vendored skill material or license changes. Broad-read truncation was recovered with focused scoped rereads, no missing evidence claimed complete. Supporting dependency/security/documentation guidance informs architecture only, not an independent security verdict. No code/scripts run. Next: primary-doc research and alternatives/proposal batch after acknowledgment.

Final checkpoint persisted: ARCH-001–005 complete; [architecture revision1](bank-ingestion-architecture.md), six decisions, Mermaid, alternatives, dependencies and complete requirement trace table saved. Official Python/SQLite/openpyxl/pdfplumber/pypdf technical sources inspected using public queries only. No private statements, Git, package installation, scripts, runtime tests, schema or implementation. Proposed feature status Awaiting Approval at architecture after Coordinator reconciliation. First multi-file save attempt failed before writing due to mismatched plan context; Coordinator verified architecture file absent, then saved it successfully separately. No dependent stage advanced during failure.

Narrow clarification persisted before presentation: Architect confirms untrusted XLSX disabled with actionable outcome unless required XML protection exists (defusedxml or verified equivalent); other formats/history remain usable. Diagram is responsibility/dataflow only, no permission for direct read/write bypass. All checklist tasks remain Done, no scope/API/version decisions added. Architecture r1 Awaiting Approval; no solution design.

## ARCH-BANK-001 r2 — 3 November 2026

BL-001 scope 8, queue 8, architecture stage. Approved input: requirements revision 4, APR-ING-REQ-004. Keep revision 1 as history. Use simple words and active voice. No code, research, table design or script commands.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| ARCH-R2-01 | Requirements 4 and architecture 1 | Read the changed rules and saved state | Done | Architect read requirements, architecture, backlog and approval records | — |
| ARCH-R2-02 | Decisions D03–D05 and diagram | Compare the range check with the earlier record check and update the plan | Done | Returned revised steps, diagram and three decisions | Coordinator saved architecture 2 |
| ARCH-R2-03 | Cases A–N | Check all cases and return approval request | Done | All cases checked; no unresolved conflict found | Architecture approval needed |

The Coordinator saved this initial plan before review. BL-001 remains In Progress at architecture. No architecture approval yet.

Final record: all three tasks complete. The Coordinator saved architecture revision 2 and kept revision 1. Decisions D01, D02, D06 and the software/file/privacy rules stay unchanged. The Architect used a focused read after a broad read ended early. No new research, code, scripts, tests or detailed design. BL-001 awaits architecture approval; queue 8 remains active.

3 November 2026: the user approved architecture revision 2. APR-ING-ARCH-002 covers the stated decisions and rules. The Coordinator recorded approval. The next separate task prepares the detailed design. The earlier pending states remain historical records.
