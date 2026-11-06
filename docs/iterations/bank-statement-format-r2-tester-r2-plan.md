# Bank statement format revision 2 — Tester repair re-check

Assignment TEST-BANK-FMT-002 r2. Backlog BL-001, scope revision 9. Verify only the latest date-error location and posting-date overlap fixes. Design revision 6 is approved as APR-ING-DES-007; revised implementation approval APR-ING-IT4-002 remains pending. Do not test or approve amount-evidence/Excel-epoch implementation because it has not started.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| TR2-001 | Current six file hashes | Compare workspace hashes to Developer plan | Done | All six hashes match the focused-fix block. The developer plan has older conflicting hash sections; Coordinator must update its current table. | Reconcile plan before final review. |
| TR2-002 | Date error location | Run focused location test or nearest behavior test | Done | `test_failed_conversion_does_not_save_supplied_normalized_values` sets an amount cell location, omits date location, and asserts `FormatError.errors[0]['location'] == 'row:3'`. | — |
| TR2-003 | Posting-date overlap | Run changed test that supplies raw posting date and reaches overlap logic | Done | `test_reliable_reference_changes_in_overlap_require_correction` passed with raw date and format inputs. | — |
| TR2-004 | Result | Report focused count and limits | Done | Prepared-env run: 3 tests and 3 subtests passed, including an adjacent invalid-date no-save case. No source/test edits or installs. | Await revised implementation approval and later full verification. |

## Initial checkpoint

The Tester first reported a three-test run for adjacent reader date-role cases before checkpoint acknowledgment. After the Coordinator saved and acknowledged this checklist, the Tester ran the overlap, date error-location and adjacent invalid-date tests: 3 passed and 3 subtests passed. The current hashes match the focused-fix block in the Developer plan. No source/test edits or installs.
