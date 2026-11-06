# Bank statement format revision 2 — Code review repair check

Assignment REVIEW-BANK-FMT-002 r2. Backlog BL-001, scope revision 9, focused review of two fixes. Related approval APR-ING-IT4-001; design revision 6 is APR-ING-DES-007, while its revised implementation scope APR-ING-IT4-002 is pending. Amount evidence and Excel epoch behavior are not yet implemented.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| CRR2-001 | Current helper and test hashes | Reconcile with Developer plan | Done | Hashes for helper, `test_bank_history.py` and `test_import_files.py` match the focused-fix hash block. The Developer plan's later final hash block is stale and needs reconciliation. | Update latest hash table. |
| CRR2-002 | Date `FormatError` location | Check fallback points to row when the date location is absent and amount-cell location exists | Done | Code fix is present. No regression assertion checks the reported location; the existing invalid-date test checks only the exception and no-save result. | Developer must add assertion before closure. |
| CRR2-003 | Posting-date overlap fixture | Check fixture supplies raw date and format so it reaches overlap logic | Done | Fixture supplies raw posting date and `%Y-%m-%d`; review confirms the covered-record comparison reaches the intended conflict path. | — |
| CRR2-004 | Focused review result | Record which findings are closed and any remaining limits | Done | Needs changes: add a regression assertion for the reported location and reconcile the Developer plan's final hash table. Amount-evidence and Excel-epoch findings remain open pending APR-ING-IT4-002. Reviewer did not rerun tests. | Complete after repair. |

## Initial checkpoint

The reviewer sent a focused re-review checkpoint. This assignment does not re-evaluate pending amount-evidence or Excel-epoch changes. The Coordinator must acknowledge this saved checklist before review starts.
