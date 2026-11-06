# Bank ingestion detailed design — plan

Assignment DESIGN-BANK-001 r1; 3 November 2026; BL-001 scope 8, active queue 8. Approved inputs: requirements 4/APR-ING-REQ-004 and architecture 2/APR-ING-ARCH-002. Stage: solution/UI design. No new screen planned. The detailed design needs separate approval.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| SD-01 | Approved inputs and project records | Read requirements, architecture, rules and relevant files | Done | Specialist read approved inputs, rules, project setup, install guide and PDF/XLSX guidance | No scripts run |
| SD-02 | Evidence record | Report confirmed inputs and conflicts | Done | Requirements 4/architecture 2 approvals agree; Python minimum 3.13; earlier state notes are history | Coordinator saved this record |
| SD-03 | Detailed design | Define records, commands, checks and recovery | Done | Proposed records, commands, limits and recovery returned | Coordinator review |
| SD-04 | Requirement checks | Check all 14 requirements and cases A–N | Done | Specialist mapped all requirements and cases | No runtime tests |
| SD-05 | Handoff | Return document and diagrams | Done | Coordinator saved bank-ingestion-solution.md revision 1 for review | Check command coverage before approval request |

The Coordinator saved this plan before review. The specialist has not read project files yet. No direct file changes, code, scripts, tests or new agents. Use simple words and active voice. Keep the approved date-range check and correction process.

Evidence record: SD-01 and SD-02 complete. The specialist found no conflict in the current approvals or item state. Earlier notes describe earlier stages. The requirements introduction needs its approval summary updated to mention architecture approval; this is not a requirement change. No private statement samples or tested reading/recovery behaviour exist. Save this record before the design work. No files changed by the specialist.

Final record saved: the specialist completed SD-01–05 and returned the proposal. The Coordinator saved the detailed design for review. Unknown-period entries remain available but separate from counted activity until period/repeat checks pass. No code, SQL, scripts, tests or file edits by the specialist. Detailed design approval remains separate. The Coordinator must check the complete command process before presentation.

## Review corrections — same proposed revision 1

The Coordinator found missing setup commands, incomplete command examples, a package naming issue, missing number/error rules, missing retry checks for changed readers, and unclear preview steps. The first proposal is saved, but it is not ready for approval.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| RD-01 | Setup and import commands | Define actions and answer/plan examples | Done | Explicit actions, issue types and complete unknown-period path | Saved in section 14 |
| RD-02 | Files, exact values and record checks | Resolve names, number output, repeat identity and key checks | Done | Launcher/package names, money strings, extraction runs, key checks and request limit | Saved in section 14 |
| RD-03 | Replacement and deletion | Define preview and apply steps | Done | Preview scope, recovery choice, explicit user instruction and stale-preview checks | Saved in section 14 |
| RD-04 | Review coverage | Check all seven findings and return wording | Done | Specialist returned a seven-point coverage table; Coordinator saved additions | Final wording checks |

No code, tests or new research planned. Keep requirements 4 and architecture 2 unchanged. The Coordinator saved this checklist before correction work.

The Coordinator saved all review corrections. They complete the same proposed design revision 1. Setup commands and unconfirmed-entry handling now have a complete path. No approved rule changed. No code or tests. Final review must keep revision checks and correction field lists precise before presentation.

## Final command checks

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FC-01 | Revision and replay rules | Define which changes advance the revision and how retries work | Done | Fact changes advance revisions; plan logs do not invalidate themselves; replay returns original result | Saved in section 15 |
| FC-02 | Preview and correction fields | Use one expected revision field and fixed correction fields | Done | One common revision field; fixed edits; known recovery choice before apply | Saved in section 15 |
| FC-03 | Setup and correction paths | Check first account evidence and replacement staging | Done | Direct user evidence allowed; replacement imports stage only | Saved in section 15 |

The Coordinator saved this checklist. No research, code or tests. Keep the same proposed revision 1.

The Coordinator saved the final command rules. All listed design tasks have a returned proposal. No implementation or tests. The remaining check is that deliberate deletion includes selected old values and temporary copies, not only active records.

The designer confirmed complete deletion scope. The Coordinator saved it: include selected historical values, observations, answers, corrections, work/evidence files and sensitive logs or receipts. Disclose any selected data retained in shared sources or snapshots. No new requirement. All review tasks are complete. Detailed design revision 1 awaits approval. No code, tests or new research during corrections.

## DESIGN-BANK-001 r2 — simplify the first version

The user says the first version has too many parts. This request concerns the design, not only the wording. The current design has 18 tables and 22 commands. Keep approved requirements 4 and architecture 2 unless an explicit change proposal identifies what to defer.

| Task ID | Deliverable | Planned action | Status | Result and evidence | Next action |
|---|---|---|---|---|---|
| R2-01 | Current design and approved rules | Read the files and simplification instructions | Done | Specialist read design 1, approved inputs and simplification instructions | Saved |
| R2-02 | Reduction list | Identify parts to keep, combine or defer | Done | Eight tables, five commands and two Python files; extra controls removed | Saved |
| R2-03 | Small first version | Check each approved requirement against it | Done | All ING-001–014 and ING-010-A–N retained | No approved input change |
| R2-04 | Single short design | Return replacement document and approval scope | Done | Single replacement design revision 2 saved | Await design approval |

The Coordinator saved the initial plan. No code, tests or new agents. Do not create another design reference file. Use diagrams, tables and short bullets.

Final checkpoint: the specialist returned DESIGN-BANK-001 r2. The Coordinator saved the smaller proposal in the same design file. Source retention, partial retries, range checks, exact money, protection and full deletion scope remain explicit. No code, tests or new research. No additional design/reference file.

## DESIGN-BANK-001 r3 — records and function steps

BL-001 scope 8; requirements 4 and architecture 2 remain approved. The user's “ok” accepts clarification work, not detailed design or implementation.

| Task ID | Planned action | Status | Evidence / next action |
|---|---|---|---|
| C3-01 | Check design 2 and approved inputs | Done | Read design 2 and approved inputs |
| C3-02 | Separate statement records from accepted reporting transactions | Done | Eight tables retained; accepted fields and source links defined |
| C3-03 | Define function inputs and results, including maintenance | Done | Four main and eight supporting functions; save repeats checks |
| C3-04 | Check four import examples; return concise text | Done | Four proposed examples checked and saved; no runtime tests |

Coordinator saved the specialist plan before continuation. No code, tests, research or new design file.

Final r3 checkpoint: Coordinator saved the specialist proposal in the existing single design file, checked accepted/source field separation and save-time checks, and removed a needless correction-staging choice from standard imports. User “ok” authorised these clarifications only. Detailed design revision 3 awaits approval. No code, tests, research or additional design document.

## DESIGN-BANK-001 r4 — library declarations

BL-001 scope 8, queue 8. Design 3 approved APR-ING-DES-003. The user requests inline library declarations and corresponding plan changes. No iteration or development approval exists. Preserve requirements 4, architecture 2 and the rule against silent installation.

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| P4-01 | Read current design and iteration plan | Done | Specialist read design 3 and iteration plan 1 |
| P4-02 | Define inline library lists and explicit preparation | Done | PEP 723 declarations, imports, uv prerequisite and explicit setup; no silent installation |
| P4-03 | Return exact changes and approval notes | Done | Coordinator saved design 4 and iteration plan 2; no implementation approval |

Coordinator saved the initial checklist before specialist continuation. Official Agent Skills and uv guidance were checked by Coordinator; no runtime behaviour has been tested.

Final checkpoint: specialist returned exact changes without editing files or running tests. Coordinator saved the narrow user-requested update in the same design and iteration records. Approved behaviour remains unchanged. Step 1 approval remains pending.

Saved-document check: specialist reported Pass after reading design 4 and iteration plan 2. Inline lists/imports, explicit uv setup, absent requirements.txt file, no installation/network during reads, independent history functions, prior approval and pending step 1 agree. No runtime tests.
