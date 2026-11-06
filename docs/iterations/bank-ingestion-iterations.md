# BL-001 — Implementation steps

Revision 2. 4 November 2026. **Status: step 3 implementation approved under APR-ING-IT3-001**, user message “continue with step 3 development”. Step 1 approval APR-ING-IT1-001 and step 2 approval APR-ING-IT2-001 remain recorded.

BL-001 scope 8; queue 8. Approved inputs: [requirements 4](bank-ingestion-requirements.md), [architecture 2](bank-ingestion-architecture.md) and approved design 3 with the user-requested library setup update in [design 4](bank-ingestion-solution.md). Approval references: APR-ING-REQ-004, APR-ING-ARCH-002 and APR-ING-DES-003. APR-ING-IT1-001 permitted step 1. APR-ING-IT2-001 now permits step 2 implementation and its checks only.

## Proposed sequence

Each step needs tests, independent reviews and a saved completion record. Ask for approval before starting the next step. APR-ING-IT3-001 authorizes step 3 development and checks for the saved scope below. The prior step 2 review checked its frozen 873-line helper; the current helper includes unreviewed step 3 work. Do not treat the earlier review as covering the current file. Step 3 must test and review the actual combined source before completion.

| Step | Goal and requirements | Files | Main checks |
|---|---|---|---|
| **1 — Saved history and import checks** | Eight approved tables; accounts/cards; exact money; balances; header periods; source records; range checks and per-file saving. ING-002–010 and applicable ING-013/014. | New `skills/bank-statement-ingestion/scripts/bank_history.py`; new `tests/bank_statement_ingestion/test_bank_history.py` | All ING-010-A–N; exact amounts and separate currencies; two cards on one account; dated balances; unknown values; empty periods; partial coverage; identical valid purchases; interrupted copies/saves and safe retry; inline Python version and empty dependency list; no external imports or automatic setup |
| **2 — File reading and complete import** | Protected PDF/CSV/XLSX reading and source evidence. ING-001/003/004/007–010/013/014. Requires completed step 1 and separate approval. | New `skills/bank-statement-ingestion/scripts/statement_reader.py`, `tests/bank_statement_ingestion/test_statement_reader.py`, `tests/bank_statement_ingestion/test_import_files.py`; update step 1 files | Generated text PDF/CSV/XLSX files; header evidence; missing/conflicting dates; empty statements; source locations; overlap; separate accounts/scopes; batch failure; formula cells; unsupported scans; all reader limits; inline libraries and checked pinned versions; explicit uv setup; calls through prepared Python; missing-software results; no installation or network access during module imports or statement reads |
| **3 — Corrections, recovery and skill use** | Corrections, export/restore/deletion, agent instructions and catalogue entries. ING-011/012/014; verify ING-001–014 together. Requires completed step 2 and separate approval. | Update `bank_history.py`, `test_bank_history.py`, `test_import_files.py`; new `tests/bank_statement_ingestion/test_maintenance.py`, `tests/bank_statement_ingestion/test_distribution.py`, `skills/bank-statement-ingestion/SKILL.md`; update `README.md`, `skills/CATALOG.md` | Explicit replacements; old values/evidence; stable IDs; coverage changes; preserved settings; reports marked out of date; recovery copies and restored sources; damaged history; selected deletion; declined backups; retained shared copies; external originals; installed skill use |

Short filenames in step 3 refer to the full paths in steps 1–2. Tests stay outside the distributed skill. Use a temporary installed copy for checks that run the skill; never use a normal user configuration.

Step 3 must also check that skill instructions state the `uv` prerequisite, the checked setup method and the prepared Python interpreter. Require explicit setup authorisation before downloading software. Keep ordinary Python imports in the scripts. Do not distribute `requirements.txt` or separate library/lock files.

Step 1 uses synthetic source evidence. It does not deliver a document reader or a complete user-facing skill. Partial work must not be presented as the finished feature.

## Checks and reviews

- Developer changes only files approved for the current step and records the actual file list.
- Tester independently checks acceptance and failure cases. Code Reviewer checks each changed file and unnecessary complexity. Security Reviewer checks each changed file, file access, source data handling and failure behaviour.
- Fixes need new checks for affected behaviour. Include all changed planning and documentation records in review lists.
- Use Python 3.13 or later. Run focused tests and lint changed Python files. At completion, run the new tests together and applicable existing checks. Report missing dependencies separately from test failures.
- Generate synthetic statement files in temporary folders. Keep fixture creation in test files. Do not use real bank data or add another production Python file.
- Preserve all approved limits and rules. No installer, `pyproject.toml`, `uv.lock`, existing document-skill or unrelated file changes. Return a proposed scope change if required.
- Coordinator alone saves backlog, lifecycle, approvals and specialist plans. Mark BL-001 Done only after all steps, tests and both independent reviews agree.

## Inspected baseline and limits

Product Owner ITER-BANK-001 r1 inspected approved inputs, skill files, catalogues, Python setup, existing tests and licences. No bank statement skill exists. Python requires 3.13 or later. Existing tests use per-skill folders; this plan instead creates a root test folder to keep tests out of installed skills. Existing PDF/XLSX licences prohibit copying their material; write new code and refer to installed capabilities. Catalogue counts are stale; change only directly affected information.

No code or tests ran during planning. The examples and checks above describe required future evidence.

**Approval record:** APR-ING-IT1-001 approved step 1 and its two implementation/test paths, plus required planning records and independent checks. Step 1 is now complete. This does not approve steps 2–3, normal user installation or another backlog item.

Revision 2 applies the user's library setup request. It removes the proposed requirements.txt file and changes setup checks. It adds no production file, command router or automatic installation. Step 1 later received APR-ING-IT1-001; later steps need separate approvals. Sources and limits are in design revision 4. No code or setup ran during planning.

## Step 1 progress

| Check | Status | Evidence |
|---|---|---|
| Approval | Done | APR-ING-IT1-001, user “approved.” |
| Developer baseline | Done | DEV-BANK-001 r1 D1 saved in bank-ingestion-step-1-developer-plan.md; Python 3.14.4 and pytest available; ruff absent |
| Implementation and focused tests | Done | DEV-BANK-001 r1: two new files; 33 tests and 7 subtests pass; both compile; ruff unavailable |
| Independent testing | Passed | TEST-BANK-001 r4: 41 suite tests, four original and three separate review-repair checks pass; both files compile; actual final source hashes verified; ruff not run |
| Independent code review | Passed | REVIEW-BANK-001 r1: 19 full artifacts and repair diff reviewed; three P2 findings fixed; simplicity passed; artifact-only access limit recorded |
| Independent security review | Passed | SEC-BANK-001 r1: all 13 changed paths current-content Pass; no findings; supplied-artifact/no-original-document-diff limits recorded |
| Completion and next approval | Done | Step 1 complete after tests/code/security reviews; step 2 awaits separate approval |

## Step 1 completion and next decision

Implemented only the approved helper and synthetic tests. Independent results: 41 suite tests, four original failure checks and three separate code-review repair checks pass; both files compile; actual final source/test hashes verified. Earlier failures remain in specialist records. Code/simplicity and security reviews pass. ruff was unavailable and did not run. Reviews used complete supplied artifacts checked against independently verified source hashes; no original document comparison was available to Security Reviewer.

The helper is a foundation, not a complete installed skill. It checks caller-supplied evidence; step 2 must connect protected readers. BL-001 remains unfinished.

**Step 2 approval:** APR-ING-IT2-001, user “yes”, approves step 2 as defined in the table: PDF/CSV/XLSX reading, inline library declarations and explicit setup checks, with its listed source/test files and independent verification. Step 3 and normal user installation remain separate.

## Step 2 progress

| Check | Status | Evidence |
|---|---|---|
| Approval | Done | APR-ING-IT2-001, user “yes” |
| Developer baseline | Done | Existing tools and source hashes checked; minimal temporary setup announced/saved before download |
| Implementation and focused tests | Done | DEV-BANK-002 r1: five scoped files; 70 tests/46 subtests, seven earlier probes and compilation pass; ruff unavailable |
| Independent testing | Passed | TEST-BANK-002 r2: date-role failures repaired; 73 tests/46 subtests, independent cases, compile and actual five hashes pass; reduced-limit/network/ruff limits recorded |
| Independent code review | Superseded | The r2 review covered the frozen step 2 source. Step 3 review r4 covers the current combined source and passed. |
| Independent security review | Superseded | Step 2 review scope was frozen; step 3 security review r2.1 covers the current combined source and passed. |
| Completion and next approval | Done | BL-001 completed after step 3; next item is not active |

## Step 3 complete — 4 November 2026

Step 3 is complete. The Tester reports 122 tests and 69 subtests passed; compilation passed. Ruff was unavailable. Code review r4 and final security review r2.1 passed. Security fixes include stored-path checks, fail-closed permission checks and account-scoped change history. The skill instructions, README and catalogue now cover the approved features. Tester and security records explain that a file cannot contain its own final hash; reviewers checked those records by content. Tests used synthetic data only. Host-wide network isolation and real bank statement layouts were not tested.

BL-001 is Done. The approved queue revision and ranks remain unchanged. No next backlog item is active.

## Format handling follow-up — 5 November 2026

The user requested support for fixed date and money format keys, exact script conversion, source evidence retention and partial import when some rows need user confirmation. This work refines the existing ING-001/003/004 acceptance within BL-001; it does not start the next backlog item. The Coordinator saved [format handling checklist](bank-statement-format-iteration.md) before code work. It requires review of the current reader, validation, save flow and skill instructions, with no history-format or protection change unless needed.

### Completion

The Developer updated `bank_history.py` and the ingestion skill. The reader and database format remain unchanged. Scripts convert raw values through fixed keys, check signs and ambiguous date-order evidence, keep original fields and locations, and leave unclear rows for user confirmation while saving clear rows. Failed conversions do not save caller-supplied normalized values. Retry identity remains stable after the user supplies a format answer.

The focused independent tests passed: 6 tests and 13 subtests. The full four-file run passed 133 tests and 124 subtests; 10 XLSX tests stopped because `defusedxml==0.7.1` is missing. Compilation and `git diff --check` passed. Ruff is unavailable. Code and security reviews passed after two repairs. One low-priority duplicate check remains. Original pre-edit source copies were unavailable, so reviewers did not verify a byte-level before/after diff. No install or real statement was used.

BL-001 is Done. No next backlog item is active.

## Step 4 — flexible field formats

**Status: paused for design clarification approval.** APR-ING-IT4-001 approved the six-file scope. Independent reviews found that amount separator meaning needs evidence and Excel serial conversion needs a checked workbook epoch. Design revision 6 is saved as a proposal in the same design document. The amount-evidence rule clarifies revision 5; the reader epoch output adds a file outside this plan. The user must approve design revision 6 before the Coordinator writes a revised implementation plan for separate approval. BL-001 scope revision 9; backlog revision 11; approved queue revision 9. Scope 8 remains complete.

### Revised step 4 proposal — evidence checks and saved tests

**Status: complete.** The user approved design revision 6 as APR-ING-DES-007 (“approved both”) and this revised implementation plan as APR-ING-IT4-002 (“Approve revised step 4”). Implementation, tests and independent reviews are complete.

| File | Planned change |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | Keep dynamic date and amount strings. Add amount-format evidence validation, checked reader epoch, clearer field location errors, and whole-statement stop for evidence or epoch failures. |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | Return the workbook's 1900/1904 epoch with protected XLSX reading metadata. Keep source reading and safety rules. |
| `skills/bank-statement-ingestion/SKILL.md` | Explain amount evidence and Excel epoch checks, with clear retry steps. |
| `tests/bank_statement_ingestion/test_bank_history.py` | Test amount ambiguity evidence, epoch match/mismatch and no-save, correct error locations, and the posting-date overlap path. |
| `tests/bank_statement_ingestion/test_import_files.py` | Test protected reader epoch output and styled/un-styled Excel date cases. |
| `tests/bank_statement_ingestion/test_maintenance.py` | Check new metadata does not change history maintenance behavior. |
| `tests/bank_statement_ingestion/test_distribution.py` | Check the installed copy includes the final instructions and scripts. |
| `.gitignore` | Keep `/tests/` ignored except `tests/bank_statement_ingestion/`, so the approved tests appear in project changes. |

### Acceptance checks

- Ambiguous amount separators need source evidence that the script checks or a user answer that names all three amount format values. Missing or conflicting evidence raises `FormatError` and saves no transaction or coverage.
- Clear amount formats may pass without extra evidence. Keep exact decimal conversion, supported separator marks and the 100-character date-pattern limit.
- The protected reader reports the XLSX epoch. The supplied `excel_serial_1900` or `excel_serial_1904` value must match it. A styled date cell must also have a matching canonical date. Missing or conflicting evidence raises `FormatError` before any financial write.
- Both matching epochs pass. Wrong epoch, absent styled canonical date, invalid/non-numeric serial and bad amount evidence stop the whole statement. Other text date patterns remain supported.
- Correct the overlap fixture so it reaches its intended duplicate/correction check. Add a date error case that confirms the reported location points to the date row when no date cell location is supplied.
- Run focused and four-file tests, compilation, `git diff --check`, and Ruff if available. Review every changed file again. Record that tests are now tracked.

This approved step does not change database format, history schema, dependencies, installers, normal user installation or other BL-001 behavior. No next backlog item is selected.

### Revised step 4 completion

| Check | Result |
|---|---|
| Approval | APR-ING-DES-007 and APR-ING-IT4-002 recorded. |
| Developer work | Amount evidence, exact separator evidence parsing, XLSX epoch checks, duplicate workbook-property rejection, structured errors for malformed date format inputs, and tracked tests completed. Date-error locations and overlap fixture were corrected. |
| Tests | Final Coordinator run: all five bank statement test files passed, 157 tests and 166 subtests. Compilation and `git diff --check` passed. Ruff unavailable. |
| Code review | Passed after parser, malformed format and no-save test repairs; see [code review plans](bank-statement-format-r3-code-reviewer-plan.md) and [parser review](bank-statement-format-r2-code-review-plan.md). |
| Security review | Passed after malformed format and duplicate workbook property repairs; see [security plans](bank-statement-format-r3-security-reviewer-plan.md) and [re-check](bank-statement-format-r3-security-reviewer-r3-plan.md). |
| Limits | No real statement/history, install, or external data used. Other workspace changes remain outside this step. |

BL-001 scope revision 9 is Done. No next item was selected by this work.

Baseline checked on 5 November 2026:

| File | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `3e550293bbbb12659f9f6e373a172d7e0cf409c42c5223b1ef4c437f72f9d1d7` |
| `skills/bank-statement-ingestion/SKILL.md` | `938035ee02a55747974b055f3c090313301b17bf3616410c5e83c21bc3305f63` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `a601c5983a40d24316366ae434def7218e10875aa9bd7c8d44340000b85bad65` |
| `tests/bank_statement_ingestion/test_import_files.py` | `a568d5eb45d41737674d5db44ca6bd1cfd2773f8397c192ff7084821f476f3d1` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `f01a87a657a848bf8698625b626b9a556e1113a4d1b9b77fe2eaf47c45fb4c9a` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1806b6a3c7c89ef62adb571dcec05a3d7901803c5dfc7499b6f59f590d3d1dec` |

The test folder is ignored by Git. The implementation must still report its changed tests and check their hashes from the workspace.

| Goal | Files | Work and checks |
|---|---|---|
| Replace fixed date/amount keys with LLM-supplied string variables and stop a statement on a format error. | `skills/bank-statement-ingestion/scripts/bank_history.py`; `skills/bank-statement-ingestion/SKILL.md`; `tests/bank_statement_ingestion/test_bank_history.py`; `tests/bank_statement_ingestion/test_import_files.py`; `tests/bank_statement_ingestion/test_maintenance.py`; `tests/bank_statement_ingestion/test_distribution.py` | Date strings use checked `strptime` patterns and `strftime('%Y-%m-%d')`. Amount strings give decimal mark, group mark and group sizes; conversion uses exact decimal text and `Decimal`. Raise a structured `FormatError` with field, raw value, format values, source location, cause and next step. A format failure stops the entire file before any financial rows or coverage are saved. Keep source, sign, date-order, exact-money, account and history checks. Update skill examples and `Record` docstring. |

### Acceptance and checks

- Accept multiple explicit date patterns, both Excel serial bases, decimal/group separators and group sizes `3` and `3-2`.
- Reject unknown date directives, invalid format variables, invalid dates, bad grouping, separator conflicts and excess money precision. Do not guess or round.
- If one format fails in a multi-row statement, raise a structured error and save no transaction, unresolved financial row or verified coverage from that statement. Preserve older accepted history and the existing failure audit behaviour.
- Keep partial imports for other unresolved causes that are not date/amount format failures.
- Test retry with a corrected format. Check error fields and source locations.
- Run the focused tests, the four relevant test files, compilation and `git diff --check`. Run Ruff if available. Use generated files and the existing prepared environment; do not install software or use a real history.
- Obtain independent code and security reviews for every changed file. Record test-directory ignore behavior and any unavailable checks.

The original approved step excludes reader change, database format change, migration, new dependency, installer change and normal user installation. Any reader change remains unapproved until design revision 6 and a revised implementation plan receive separate approval. The next backlog item remains unselected.

