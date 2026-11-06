# Backlog workflow implementation — revision 1

Assignment: implement the user-approved backlog-aware Product Owner workflow.
Baseline: existing agents, commands and planning skills; unrelated tool deletions and .idea files excluded.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| BL-001 | Commands and Product Owner | Add discovery and backlog-aware selection | Done | commands/backlog.md, commands/plan.md, agents/product-owner.md updated | — |
| BL-002 | Coordinator and specialists | Persist backlog checkpoints and queue state | Done | Coordinator and all eight specialists follow shared checkpoint contract | — |
| BL-003 | Planning skills and README | Align shared contract and examples | Done | Four planning/documentation skills and README aligned | — |
| BL-004 | Changed-file inventory | Check contracts, frontmatter and scenarios | Done | git diff --check passed; frontmatter/permission/routing/coverage assertions passed | — |

No runtime harness execution or installation is part of this assignment.

## Verification and limits

Static scenario review: existing match reuses ID; unmatched direct request persists before requirements; absent file is created; ambiguous/Done matches require clarification; active-feature conflict asks switch-or-queue. Discovery produces Proposed records; approval targets identified scopes. Queue aliases resume active work, respect dependencies and downstream approvals, and exclude unapproved revisions. Failed persistence blocks advancement. Every specialist reports checkpoints; only reconciled feature completion becomes Done.

All modified existing agent/command/skill frontmatter preserved; permission JSON valid for all nine agents. Installer files and unrelated pre-existing tool deletions left untouched. No harness execution, external research run or installation performed: verification covers distributed instructions, not demonstrated runtime compliance. No executable application logic changed.
