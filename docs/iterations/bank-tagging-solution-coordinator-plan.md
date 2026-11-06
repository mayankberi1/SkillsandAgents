# BL-009 solution design — Coordinator checklist

Assignment COORD-DESIGN-BANK-009 r1. Backlog revision 8; BL-009 scope revision 2. Requirements revision 1 is approved as APR-ING-REQ-005; architecture APR-ING-ARCH-003 and design revision 4 APR-ING-DES-005 are approved. Requirements revision 2 is approved as APR-ING-REQ-006; design revision 4 is approved as APR-ING-DES-005; step 1 awaits approval. Active queue item BL-009, rank 2; queue revision 8. Current stage: iteration planning.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| C1 | Reconcile stage approvals | Confirm requirements and architecture approvals and unchanged scope | Done | APR-ING-REQ-005 and APR-ING-ARCH-003 recorded | — |
| C2 | Save Solution Designer checklist | Persist the initial plan before delegation | Done | DESIGN-BANK-009 r1 saved | — |
| C3 | Review detailed design | Check data contracts, function behavior, failure paths and requirements coverage | Done | Designer r2 puts current tags on transactions, keeps one reusable-rule table, does not keep tag change history, and defines both rule scopes and deletion behavior | — |
| C4 | Record design approval and reconcile requirements | Save approval and align approved requirements | Done | User approved design revision 3 as APR-ING-DES-004; preserved requirements revision 1 and saved revision 2 to remove tag-change history | — |

No source changes or tests are authorized. Keep scope revision, rank and queue revision unchanged.

| C5 | Request requirements approval | Present the exact requirements change | Done | User approved requirements revision 2 as APR-ING-REQ-006; no code or tests | — |
| C6 | Revise iteration plan | Align the history update with the new design proposal | Done | Saved [implementation steps revision 2](bank-tagging-iterations.md); it replaces the separate-copy approach with one transaction | Request approval for step 1 |
| C7 | Record design revision 4 approval | Save user decision and update lifecycle status | Done | User approved revision 4 as APR-ING-DES-005 | — |
| C8 | Present step 1 approval | Ask for approval of the scoped development step | In Progress | Plan revision 2 lists files, tests, failure checks and independent reviews | User decision needed |
