# Amount evidence parser repair — Code review checklist

Assignment REVIEW-BANK-FMT-003 r2. Backlog BL-001, scope revision 9, P2 repair review. Approval APR-ING-IT4-002. Read-only review of `bank_history.py` and `test_import_files.py`; baseline and repaired hashes are in [the Developer repair plan](bank-statement-format-r2-developer-plan.md).

| Task ID | File / criterion | Planned action | Status | Result | Next action |
|---|---|---|---|---|---|
| CRR4-01 | Two approved files and hashes | Reconcile current hashes with Developer repair plan | Done | Both SHA-256 values match. | — |
| CRR4-02 | Exact evidence parser | Check empty, space, punctuation, malformed and repeated values; compare supplied settings exactly | Done | Splits on `; `, keeps a one-space value, rejects duplicate/unknown/missing fields and mismatches; semicolon can remain a value. | — |
| CRR4-03 | Regression test | Confirm conflicting whitespace evidence fails and saves no financial data or coverage | Done | `space-must-not-mean-empty` rejects false empty separator; failure tests check no transaction or verified coverage. | — |
| CRR4-04 | Evidence meaning and simplicity | Check source/user evidence remains meaningful and parser is clear | Done | No new finding. Source evidence is checked against protected source text and saved with quote, kind and location. | — |

## Initial checkpoint

The Reviewer read the repair plan. The Coordinator acknowledged this checklist before review. The focused review passed with no new findings. The Reviewer made no source/test changes.
