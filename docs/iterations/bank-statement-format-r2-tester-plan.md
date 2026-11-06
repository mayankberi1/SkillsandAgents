# Bank statement format revision 2 — Tester checklist

Assignment TEST-BANK-FMT-002 r1. Backlog BL-001, scope revision 9, implementation verification. Approval APR-ING-IT4-001. Independent checks of the approved format behavior. Source and test files are read-only for this assignment.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| TST-001 | Six approved paths and final hashes | Reconcile workspace hashes with Developer plan | Done | All six hashes match the Developer plan. | — |
| TST-002 | Date and money conversion | Verify custom date patterns, both Excel bases, exact amount separators and grouping `3`/`3-2` | Done | Focused checks passed for custom patterns, both Excel bases, exact amounts and both grouping styles. | — |
| TST-003 | Invalid and ambiguous formats | Check unsupported patterns, conversion failures, grouping, precision and user-confirmation errors | Done | Focused cases cover bad and ambiguous formats; 11 focused tests and 17 subtests passed. | — |
| TST-004 | Import boundaries | Check full-statement stop, no transaction/unresolved row/coverage write, corrected retry and preserved non-format partial import | Done | Focused stop/no-save, corrected retry and non-format partial-import cases passed. | — |
| TST-005 | Four assigned test files | Run all tests and compile checks; record failures and environment limits | Done | Four-file suite: 142 tests and 130 subtests passed in 5.34s. `compileall` passed for helper and four test files using `/tmp/bank-step2-reader-env`; no installs or real data. | — |
| TST-006 | Test result | Return criteria mapping, counts, hashes and limits | Done | Independent test result returned to Coordinator. The prepared environment included the XLSX dependency; no outstanding test limitation. | — |

## Initial checkpoint

The Tester read the approved Developer plan and acceptance criteria. The initial checkpoint was acknowledged before testing. Independent focused and full-suite results are recorded above. No source or test files were changed by the Tester.
