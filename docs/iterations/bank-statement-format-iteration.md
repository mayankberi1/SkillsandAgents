# Bank statement format handling — implementation checklist

Assignment COORD-ING-FMT r1. Backlog item BL-001, scope 8, implementation follow-up requested by the user on 5 November 2026. The user directly approved work to support fixed date and amount format keys, source-linked conversion, exact money, unresolved-record questions and partial imports. Preserve the database format and existing protections unless required. Use generated files only; do not install software or use a real history.

## Goal

The agent supplies each field's original text, a supported format key, source location and any sign evidence. The scripts check the source, convert values to ISO dates and exact decimal amounts, and retain original evidence. A record with unclear format or failed conversion stays unresolved and does not block clear records in the same statement.

## Baseline inventory

| File | SHA-256 before edits | Review purpose |
|---|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `817863c4487970b468cfde76610406747a98fd4c6776f01a9fdc8f3a03b90c1c` | Validation, conversion, evidence and save flow |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `05588dd5eea9b3db64c41b03dcf0a1b86b87afa22672fb7e41107b41484094f5` | Protected raw text and cell locations; no edit unless needed |
| `skills/bank-statement-ingestion/SKILL.md` | `07cbb82fa36587a747c453839bf409a40368421b4e1c74dbf88a5c909748fd11` | Agent contract and questions |
| `tests/bank_statement_ingestion/test_import_files.py` | `26a94c62537a0e45141b5981918072f5f96418fb9c9c791236d36f392255a830` | Generated source and partial-import cases |
| `tests/bank_statement_ingestion/test_bank_history.py` | `450c92b2a6db9bc41429f44cc2f88f99952d5753b53076fd697d0040848e1f28` | Exact conversion and save regressions |
| `tests/bank_statement_ingestion/test_maintenance.py` | `e87104f63b14e4689ebcb888a77ca60e8592fc668de1811dde726b1358924b72` | Existing correction and persistence behavior; update if needed |
| `tests/bank_statement_ingestion/test_distribution.py` | `1d0bf07a8ab4f3a265829579f2bdb581825f36ce64c3e37b62a8f4f6c054fbad` | Installed-skill text checks |

The first saved draft had a mistyped maintenance-test hash. The Coordinator checked and corrected it before edits; use the table value above.

## Work and verification

| ID | File / criterion | Planned action | Status | Result / next action |
|---|---|---|---|---|
| FMT-01 | Reader, validator, save flow | Trace raw text, cell evidence, conversion and unresolved-record paths. Keep `statement_reader.py` unchanged if it already provides required protected evidence. | Done | `statement_reader.read_statement` returns bounded fragments with source locations, cell values and raw text; XLSX exposes protected date-style metadata. `_verify_source` checks record text and source cells. `_record_problem` accepts only ISO dates and decimal-like amounts, compares amount to raw text, and handles debit signs. `_process_section` stores raw amount text, source quotation and field/sign locations, keeps unresolved records, and accepts other clear rows; verified coverage requires a complete row set. Skill currently says to interpret fields but gives no fixed keys. |
| FMT-02 | `bank_history.py` | Define a small fixed date/amount key set. Convert exact source text in the script, reject unknown or invalid keys, verify dates and currency precision without rounding, and retain raw values/keys/locations/evidence in existing records. | Done | Script converts each supported format. It rejects conflicting signs, clears unverified normalized fields and checks date-order evidence for ambiguous slash dates. No history format or reader change. |
| FMT-03 | `SKILL.md` | Tell the agent how to identify each key from evidence, provide source text/location and sign evidence, and ask the user when evidence is unclear. Explain partial-import results. | Done | Skill lists keys, tells the agent to pass original text and locations, requires evidence for ambiguous order, and explains unresolved rows and partial saves. |
| FMT-04 | Import/history/distribution tests | Test supported date and amount formats, ambiguous date order, invalid conversion, sign evidence, exact precision and partial imports with both clear and unclear records. | Done | Generated tests cover keys, amounts, evidence, invalid and ambiguous values, retry, partial saves and retention. Final four-file suite passed 142 tests and 125 subtests in the existing prepared environment. |
| FMT-05 | Checks and handoff | Run relevant tests, compile and lint where available. Inspect scope and update this checklist. Obtain independent code, test and security reviews. | Done | Code and security reviews pass. Tester and Coordinator ran the full four-file suite in the existing environment with `defusedxml==0.7.1`: 142 passed, 125 subtests. Compilation and `git diff --check` passed. Ruff unavailable. Original pre-edit source copies were not saved, so reviewers could not compare full file bytes. |

## Review repairs before approval

The independent code and security reviews found two medium integrity gaps. First, a failed conversion could leave a model-supplied normalized date or amount in an unresolved record. Second, a slash date with both day and month at or below 12 could accept either order without recorded evidence for that order. Repair within the approved scope: store only values converted from raw text; for a numerically ambiguous slash date, require a verifiable header, same-column date, or user answer that supports the selected order. Keep the raw value and evidence, leave the row unresolved when proof is missing, and add tests. The coordinator acknowledges this bounded repair before edits.

Developer assignment DEV-ING-FMT r1 and its pre-edit hashes are saved in [Developer checklist](bank-statement-format-developer-plan.md). Coordinator acknowledged the initial checkpoint. The Developer must report the source trace before edits.

## Design constraints

- Fixed format keys only. No locale guessing and no date-order guessing.
- The script converts original text. Do not accept an unchecked normalized value as proof of conversion.
- Keep source quotation, field location, raw text, key and sign evidence in current source-linked records.
- Reject excess money precision; never round.
- Preserve partial imports: save clear records, retain unclear records with a reason, and ask about only those records.
- Preserve file/hash/source checks, current transactions, database format, account boundaries and sign checks.

## Format-key checkpoint

Proposed fixed date keys: `ymd_dash`, `dmy_slash`, `mdy_slash`, `dmy_dash`, `dmy_dot`, `d_mmm_yyyy`, `mmm_d_yyyy`, `excel_serial_1900`, `excel_serial_1904`. Proposed amount keys: `decimal_dot`, `decimal_comma`, `grouped_comma_dot`, `grouped_dot_comma`, `grouped_space_comma`, `grouped_space_dot`, `integer`. Each key names one exact spelling. The LLM must use source/header context to select a key; it must ask the user if date order or separator meaning is unclear. The script must reject text that does not match the selected key and reject dates or money that exceed the accepted range/precision.

The Developer confirmed the source trace and proposed these keys. The Coordinator approves this bounded implementation choice as within the user's request. The script must derive normalized values from raw text and keys, not trust an LLM-supplied normalized value. Format keys must not prevent an unresolved source row from matching on retry after the user confirms the format.

## Review and completion

The Code Reviewer confirmed that the two findings recorded above are closed. One low-priority duplicate `raw_date is None` check remains; it does not affect results. The Security Reviewer passed all six files. The Tester independently passed 6 focused tests and 13 subtests, then passed all four test files in the existing prepared environment: 142 tests and 125 subtests. Compilation and `git diff --check` passed. Ruff is not installed. All reviews note that the original pre-edit file copies are unavailable; they checked current files against the saved baseline hashes and requirements, not a complete byte-level diff. No package or real history was used.

## Final test-fixture checkpoint

A final security recheck found two older XLSX tests that proposed a posting date without its raw text and format key. Update only those test fixtures so they reach the source-location checks under the new contract. Keep one test with a missing posting-date source location and one test that uses the same cell for both date roles. Then rerun the affected tests and the full prepared-environment suite; refresh review evidence for the test-only change.

Final date-role fixtures now include original text and fixed keys. The missing-location case still has no source location for the proposed posting date. The one-cell case uses the same verified source cell for both roles and stays unresolved. Both affected tests pass. The full prepared-environment suite passes: 142 tests and 125 subtests. `compileall` and `git diff --check` pass.

Final test hashes: `test_import_files.py` `6b3f4e69b11deb50156b781f41b1d664d17a2933f297edf91e3ae3b0518cb877`; all other final hashes are recorded in the previous review table. The test directory is ignored by the repository, so test edits do not appear in normal `git status` output.

Reviewer follow-up: the two posting-date fixtures now use the same raw serial `46037` and `excel_serial_1900` key as the XLSX source. This removes a text mismatch as a reason for rejection. The tests now focus on the missing posting-date location and reuse of one cell for both date roles. Both tests and the full suite pass again. Final `test_import_files.py` SHA-256: `4c98ecbad70a37f9b46fd7b2f256b56f8b0296116921b700b451bf1add640049`.

Final fixture correction: the missing-location XLSX now has separate Date and Posting date columns, both with source serial `46037`; the record gives only the transaction-date cell location. The one-cell test uses that same serial/key for both roles and points both roles to one cell. This lets the tests reach the intended location and duplicate-cell checks. The two focused tests pass; the full suite passes with 142 tests and 125 subtests. Final test hash: `99a12b9c76e3395a2d880a09f7734b01db5f64ea27c78c29b8b4036dbe42c63f`.

Final reviewer-driven test correction: the unique Posting date cell case now places Amount in the column selected by the test helper and expects the script to infer the unique posting-date cell from its heading. The one-cell case still checks that one cell cannot prove two date roles. Both focused tests pass; the full suite passes with 142 tests and 125 subtests. Final `test_import_files.py` SHA-256: `a568d5eb45d41737674d5db44ca6bd1cfd2773f8397c192ff7084821f476f3d1`.
