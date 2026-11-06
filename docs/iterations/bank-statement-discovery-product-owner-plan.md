# Bank statement discovery — Product Owner plan

Assignment: DISC-BANK-001 revision 1. Stage: discovery. Backlog IDs not yet allocated; proposed status: Proposed. Approval reference: user `/backlog` request on 2026-10-24; discovery only.

Scope: reuse document skills for statement ingestion; duplicate, unusual and recurring transactions; spend analysis; privacy. Baseline: no `docs/product-backlog.md` found. Existing `backlog-workflow-implementation-plan.md` describes workflow work, not feature backlog IDs; preserve it. No implementation or downstream approval.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| D1 | Instructions, backlog, document skills | Inspect relevant project evidence | Done | Product Owner inspected instructions, README, pdf/xlsx/docx and iteration records; backlog absent | — |
| D2 | External evidence | Research authoritative ingestion, signals and privacy sources | Done | Moneysmart, Plaid and OAIC sources recorded in backlog | Public sources only; no sample testing |
| D3 | Ranked proposal | Deduplicate scopes, assumptions and questions | Done | Five skill scopes with shared ingestion dependency returned | User decisions refine draft |
| D4 | Backlog handoff | Return concrete draft and approval boundary | Done | Final handoff received; Coordinator persists backlog | Await backlog approval |

Initial checkpoint persisted by Coordinator. No bank statement data supplied. Research must use generic public queries. Next: D1–D4 discovery batch, with final checkpoint before further advancement.

Final checkpoint: discovery tasks completed; no skills implemented and no feature marked Done. User subsequently confirmed text PDFs and CSV/XLSX first, scans later; personal bank and credit-card accounts; separate currencies. Refinement requested from Product Owner. Backlog remains Proposed. No private statement data used in research. See `../product-backlog.md` for sources, limitations and exact approval target.

Refinement checkpoint DISC-BANK-001 r2: R1 reconcile all five scopes against confirmed format/audience/currency decisions — Done; R2 return updated proposal and remaining output question — Done. Product Owner confirmed unchanged ranks/dependencies and no v1 OCR scope. Coordinator persisted refinement in backlog revision 1 draft. Duplicate and unusual analyses retain account/currency context; recurring analysis retains account context and separates currencies. No required discovery tasks remain; backlog approval and output preference remain open.
