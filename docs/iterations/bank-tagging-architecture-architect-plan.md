# BL-009 architecture — Architect checklist

Assignment ARCH-BANK-009 r1. Backlog revision 8, BL-009 scope revision 2. Requirements revision 1 approved as APR-ING-REQ-005. Queue revision 8; BL-001 Done. This assignment proposes architecture only; it does not approve detailed design or implementation.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| A1 | Approved requirements and existing design | Read BL-009 TAG-001–TAG-010 and BL-001 approved architecture/design | Done | Read requirements revision 1, BL-001 architecture 2 and design 4 | — |
| A2 | Trust and data boundaries | Trace transaction data, minimal query, web results, user answers and saved tagging records | Done | Search receives only a safe business name; user answers and saved records remain in local history | — |
| A3 | Alternatives | Compare at least two ways to perform vendor lookup; cover privacy, complexity, failure behavior and ownership | Done | Compared runner search with a controlled provider helper; recommended runner search with user fallback | — |
| A4 | Proposal | Recommend component boundaries and data flow; state assumptions, limits and decisions requiring approval | Done | Saved [architecture revision 1](bank-tagging-architecture.md); user approved option A as APR-ING-ARCH-003 | Solution design is next |

Read actual records. Do not edit files or run tests. Do not define table fields, function contracts or Python implementation; those belong to solution design after architecture approval. Do not exceed the approved requirements.

## Final handoff

Architecture proposal saved in [revision 1](bank-tagging-architecture.md). The Architect recommends runner web search when available, a safe business name as the only query, and user fallback when search is unavailable or unclear. A found vendor is a suggestion; user categories and reusable rules need confirmation. Approval is required before solution design. No code or tests.

Approval: user approved the proposal without changes as APR-ING-ARCH-003. Solution design may proceed; implementation remains unapproved.
