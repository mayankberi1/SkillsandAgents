# Bank statement format revision 3 — Developer checklist

Assignment DEV-BANK-FMT-003 r1. Backlog BL-001, scope revision 9, implementation. Approvals: APR-ING-DES-007 and APR-ING-IT4-002. Requirements 4 (APR-ING-REQ-004), architecture 2 (APR-ING-ARCH-002), design 6. This assignment changes only the eight paths listed here. Keep other workspace changes.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| FMT3-001 | Approved design, plan and eight-file baseline | Check approval, exact scope, current content and hashes | Done | Design 6 and revised step 4 plan APR-ING-IT4-002 are approved. Eight current hashes are recorded below. The date-location fix and posting-date fixture repair are present. | Wait for Coordinator acknowledgement before edits. |
| FMT3-002 | `bank_history.py` | Add amount-format evidence checks, checked XLSX epoch and canonical date checks; preserve exact conversion, source checks and whole-file no-save behavior | Done | `Record` accepts and saves amount-format evidence. Unclear amount text requires all three matching format values from a user or checked source header/record. XLSX serial dates require matching reader epoch; styled cells also require matching canonical dates. Errors use whole-statement `FormatError`. | Independent review should check evidence relevance and no-save behavior. |
| FMT3-003 | `statement_reader.py` | Return the protected XLSX workbook epoch in read metadata without changing reader limits | Done | Reader returns `workbook_epoch` as `1900` or `1904` for XLSX. Existing XML, resource and source checks remain. | Independent review should check epoch source and output. |
| FMT3-004 | `SKILL.md` | Explain when amount evidence is needed and how to use epoch evidence and retry | Done | Added explicit example syntax for evidence and whole-statement retry guidance for amount/Excel date failures. | Include in skill review. |
| FMT3-005 | `test_bank_history.py`; `test_import_files.py` | Test clear and ambiguous amount formats, matching/missing/conflicting evidence, reader epoch, canonical dates, invalid serials, whole-file stop, and text dates | Done | `test_import_files.py` adds missing, matching/conflicting user, valid/invalid source evidence, evidence save, epoch metadata, mismatch, missing canonical and nonnumeric serial cases. Existing text dates and both matching epochs pass. Existing `test_bank_history.py` remains unchanged. | Review new tests against acceptance cases. |
| FMT3-006 | `test_maintenance.py`; `test_distribution.py` | Check existing maintenance behavior and final installed skill content | Done | Existing maintenance tests pass. Distribution assertions now check amount evidence and Excel epoch instructions. | None. |
| FMT3-007 | `.gitignore` | Track only `tests/bank_statement_ingestion/` under the ignored `/tests/` folder | Done | Replaced `/tests/` with `/tests/*`, re-included `/tests/`, then re-included only `/tests/bank_statement_ingestion/`. Git ignore behavior was not checked because this role must not run Git commands. | Coordinator should verify tracked status. |
| FMT3-008 | Eight approved paths and criteria | Run focused/full tests, compilation, whitespace and available lint; report hashes and limits | Done | Four assigned test files: 144 passed. All five test files in the directory: 154 passed after the final evidence-location tightening. `py_compile` passed. Trailing-whitespace scan found none. Ruff is unavailable. Git commands, including `git diff --check`, were not run under role rules. | Send for independent review; coordinator verifies scope/tracked status. |

## Baseline inventory

| Approved path | SHA-256 | Lines |
|---|---|---:|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `bf45e43424859d1dee75f25864a3726f9a940a7192eae1b13ef40a3ccdd71006` | 1,908 |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `05588dd5eea9b3db64c41b03dcf0a1b86b87afa22672fb7e41107b41484094f5` | 305 |
| `skills/bank-statement-ingestion/SKILL.md` | `ead08a329ccf1d82db6c341d8d5474d0964eb4a585d5e2376c0a105bae704d31` | 100 |
| `tests/bank_statement_ingestion/test_bank_history.py` | `78c780cb78a0e431a81bd53ac65dd0a278801598be3cb974a281b1515cc4bbb7` | 837 |
| `tests/bank_statement_ingestion/test_import_files.py` | `be16aad146b7526afdd9eb4e9d527c6e8220c6ccbd4680820e0a587e8078d16a` | 445 |
| `tests/bank_statement_ingestion/test_maintenance.py` | `397129e10069a33ce0f73acd5b4a1bcdabec647a380e82038213dfae6cbc724b` | 688 |
| `tests/bank_statement_ingestion/test_distribution.py` | `45065c6fcc7f02de0308c3afd6184181fe81d4ad3ab40e259e5bcdaa538511b3` | 74 |
| `.gitignore` | `737a7ad36a31527e209e4a9fd2e787bfb882f3f6bc48410de12ff8e23fa35934` | 222 |

The root ignore file excludes `/tests/`. The approved test folder is therefore not tracked. `_xlsx` currently computes `epoch_1904` and uses it for `canonical_date`, but discards the epoch from reader output. `Record` has no amount-format evidence field. `_verify_source` checks source evidence and then converts fields before save. The date-error location fallback and overlap fixture are already corrected in the baseline. No code, skill, test or ignore-file edits were made for this assignment. No real statement or history will be used, and no software will be installed.

## Next action

Send the eight approved-path hashes and test evidence to Coordinator for independent review. Preserve failed attempts: the first test invocation failed because the import path omitted the test folder; the first full discovery then exposed source evidence shadowing the row reference and an overly strict styled-date location check; one compile command used a misspelled test path and failed before the corrected compile command passed. The fixes passed the final four-file run and all five test files. No Git command was run, so tracked status and `git diff --check` remain unverified.

## Final path hashes

| Approved path | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `1ecc8b5f9cb901c7be96a8d0e2bc800fdf28bc631ac61ff4531aa81935d6b44a` |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `e0c05dc1e5738a98832bcd3d7ea63e66fd9cf6a7fe07ad622508eca83750aaf3` |
| `skills/bank-statement-ingestion/SKILL.md` | `a8eaf3e06b43812615fe8570d10b8bd2d33544261014b5d0e86462d71f80490a` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `78c780cb78a0e431a81bd53ac65dd0a278801598be3cb974a281b1515cc4bbb7` |
| `tests/bank_statement_ingestion/test_import_files.py` | `9aabf02c8e1900d1d84689009dd8bc80d10be0e8ad4768f6b8715469c5f621ee` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `397129e10069a33ce0f73acd5b4a1bcdabec647a380e82038213dfae6cbc724b` |
| `tests/bank_statement_ingestion/test_distribution.py` | `b97edbae18e7f17b725e8750e45afccf3ed83a275e5bc442cd81a5a1cd5451c2` |
| `.gitignore` | `b3bb37284fa3329a19a7b3ea50e5fc08918ea138d38323a84f39446ac8f6fd0d` |
