# BL-009 step 2 — Code Reviewer checklist

Assignment REVIEW-TAG-IT2 r1. Backlog revision 8; BL-009 scope 2; queue revision 8. Requirements APR-ING-REQ-006, design APR-ING-DES-005 and step approval APR-TAG-IT2-001. Review current files and compare to Developer baseline hashes. Do not edit files or run tests.

| Task ID | File / check | Planned review | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| R2-01 | `skills/bank-statement-ingestion/scripts/bank_history.py` | Read/save behavior, validation, SQL, rule ordering support, per-item transaction boundaries, financial-field preservation | Done | Fail. At lines 1117–1122, a partial category update clears existing vendor source fields. At lines 1096–1116, a tags-only user choice can be replaced by a later rule. | Developer must fix and add regression tests |
| R2-02 | `tests/bank_statement_ingestion/test_bank_history.py` | Check meaningful coverage for accepted and rejected inputs and failure behavior | Done | Fail. Tests omit source preservation after category-only confirmation and tags-only precedence over a rule. | Add tests for both findings |
| R2-03 | New `skills/bank-transaction-tagging/SKILL.md` | Check concise, correct workflow and claims | Done | Pass. Skill states transaction choice before rules and web lookup, and separates saved/failed/unresolved results. | — |
| R2-04 | `README.md` | Check skill entry | Done | Pass. Skill is listed accurately. | — |
| R2-05 | `skills/CATALOG.md` | Check skill entry and dependency notes | Done | Pass. Skill is listed with its helper and search-tool need. | — |
| R2-06 | `tests/bank_statement_ingestion/test_distribution.py` | Check new distribution assertion | Done | Pass. Checks skill metadata, functions, privacy text and catalog entry. | — |
| R2-07 | Cross-file design and simplicity | Check contracts, errors, precedence and scope remain consistent; identify simpler safe options | Done | Fail. The code does not fully preserve user-tag precedence or source evidence for unchanged tag fields. No unnecessary abstraction or dependency found. | Re-review after fixes |
| R2-08 | Verification and changed-file evidence | Compare six current hashes to Developer baseline hashes and reconcile test evidence | Done | Pass. All six current hashes match the Developer's final values. The reviewer did not run tests. | Test claims remain Developer/Tester evidence |

No code change by Reviewer. No real history or external data.

## Review verdict

Fail pending fixes. The reviewer found two P2 defects: (1) a partial user category update can erase a web vendor's source and uncertainty; (2) a tags-only user choice can be overwritten by a later matching rule. The reviewer did not run tests, edit files, or open real history. The Tester separately found that a rule-applied vendor/category remains marked `unknown`; see the Tester plan.
