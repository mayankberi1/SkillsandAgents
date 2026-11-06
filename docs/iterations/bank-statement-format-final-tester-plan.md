# Bank statement format final — Tester checklist

Assignment TEST-BANK-FMT-005 r1. BL-001 scope revision 9, final independent test check for APR-ING-IT4-002 after R4/R5 repairs.

| Task ID | File / criterion | Planned action | Status | Result | Next action |
|---|---|---|---|---|---|
| TFIN-001 | Eight approved paths and hashes | Compare current hashes with latest Developer plans | Done | All eight hashes match the initial checkpoint; no files changed | Complete |
| TFIN-002 | Malformed formats and epoch conflict | Run malformed pair, unhashable format and conflicting workbook epoch no-save tests | Done | 3 tests passed, 4 subtests passed | Complete |
| TFIN-003 | Five bank statement test files | Run all tests in prepared environment | Done | 157 tests passed, 166 subtests passed in 6.78 seconds | Complete |
| TFIN-004 | Test report | Return counts and environment limits | Done | Tester did not run Git checks under role limits; Coordinator owns these checks | Complete |

## Initial checkpoint

The Coordinator acknowledged the checkpoint. The focused checks passed: 3 tests and 4 subtests. The full five-file suite passed: 157 tests and 166 subtests in 6.78 seconds. All eight file hashes match the initial checkpoint, so the tests made no file changes. The Tester did not run Git checks under role limits. The Coordinator had already run `git diff --check`; it passed. Ruff was unavailable. The workspace has unrelated changes outside this task; they remain untouched.
