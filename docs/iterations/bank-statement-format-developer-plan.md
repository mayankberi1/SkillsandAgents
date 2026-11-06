# Statement format handling — Developer checklist

Assignment DEV-ING-FMT r1. BL-001 scope 8; user direct request on 5 November 2026. Follow the approved [format handling checklist](bank-statement-format-iteration.md). Use generated sources only. Do not install software or use real history.

## Baseline confirmed before edits

| File | SHA-256 |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `817863c4487970b468cfde76610406747a98fd4c6776f01a9fdc8f3a03b90c1c` |
| `skills/bank-statement-ingestion/scripts/statement_reader.py` | `05588dd5eea9b3db64c41b03dcf0a1b86b87afa22672fb7e41107b41484094f5` |
| `skills/bank-statement-ingestion/SKILL.md` | `07cbb82fa36587a747c453839bf409a40368421b4e1c74dbf88a5c909748fd11` |
| `tests/bank_statement_ingestion/test_import_files.py` | `26a94c62537a0e45141b5981918072f5f96418fb9c9c791236d36f392255a830` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `450c92b2a6db9bc41429f44cc2f88f99952d5753b53076fd697d0040848e1f28` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `e87104f63b14e4689ebcb888a77ca60e8592fc668de1811dde726b1358924b72` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1d0bf07a8ab4f3a265829579f2bdb581825f36ce64c3e37b62a8f4f6c054fbad` |

## Work checklist

| ID | Planned action | Status | Result / next action |
|---|---|---|---|
| FMT-DEV-01 | Trace reader, raw fragments, source verification, unresolved rows, validators and save transaction. | Done | Confirmed reader source locations and hash checks, normalized-only validation, unresolved-row handling, and atomic per-file save. Existing `source_location` JSON and `amount_text` can retain the added details without a schema change. |
| FMT-DEV-02 | Add fixed keys and exact conversion/validation to the existing ingestion script; preserve current source-linked fields and format 2. | Done | Added fixed date/amount keys. The script derives values from original text, checks sign evidence and precision, stores field text/key/location in existing source-linked records, and keeps retries linked when a format key is supplied later. `statement_reader.py` and database format 2 remain unchanged. |
| FMT-DEV-03 | Update the ingestion skill with per-field keys, source locations, sign evidence, clarification and partial-result steps. | Done | Added all approved key definitions, evidence rules, unresolved-record reporting and user questions. |
| FMT-DEV-04 | Add/update generated tests for supported formats, ambiguous dates, invalid conversions, sign evidence, exact precision and partial imports. | Done | Added generated CSV format cases, ambiguous/invalid cases, exact precision, partial import, source evidence retention, retry identity and direct Excel serial conversion checks. Existing tests now supply explicit original text and keys. |
| FMT-DEV-05 | Run relevant tests/compile/lint if available; inspect scope and report evidence/limits. | Done | Initial results are kept below as history. The final results after two review repairs are in [Final bounded repair checkpoint](#final-bounded-repair-checkpoint). |

Developer confirmed that all seven hashes match the Coordinator baseline. The Coordinator acknowledges the initial assignment checkpoint. The Developer completed FMT-DEV-01 and returned the source trace. The Coordinator acknowledges this checkpoint and approves the fixed format-key list in the [main checklist](bank-statement-format-iteration.md). Implementation may proceed. Preserve answer/retry matching when the format key changes: the source row identity must not depend on the later format choice.

## Review finding before final verification

The Coordinator found that debit/credit evidence can replace an explicit `+` or `-` in the source amount, even when the two signs conflict. This can change the saved amount without user confirmation. Fix only this case: compare an explicit source sign with the sign evidence; keep the row unresolved on conflict. Add one regression test. Do not change other behavior. The Coordinator acknowledges this bounded repair before edits.

The repair is complete. `+10.00` with `Debit` now stays unresolved with a conflict reason. The focused set passes 9 tests and 18 subtests; Python compilation passes. Ruff is not installed. No package was installed. Fresh hashes: `bank_history.py` `8b837e0a962f8770427985402f08a9a64468046c392fb374491ab63508c466b7`; `test_import_files.py` `8e9a5355266eb717e62d721c744f0061d8fe6d7ba782193f726fa7da6377411d`.

## Independent review findings before approval

The Code Reviewer found that failed conversion leaves caller-supplied normalized fields on an unresolved record. The Security Reviewer found that the script accepts either slash-date order for a value such as `04/05/2026` without checking evidence for that order. The Coordinator saved both findings in the main checklist and acknowledges these bounded repairs before edits: retain only normalized values the script converted; require verifiable date-order evidence for ambiguous slash dates; keep the raw fields; leave the row unresolved when proof is missing; add regression tests. Do not change the history format or reader.

## First verification before review repairs — historical

Focused command:

```sh
python3 -m pytest tests/bank_statement_ingestion/test_import_files.py::ImportTests::test_supported_date_and_amount_keys_convert_from_source_text tests/bank_statement_ingestion/test_import_files.py::ImportTests::test_ambiguous_date_and_invalid_values_stay_unresolved tests/bank_statement_ingestion/test_import_files.py::ImportTests::test_retry_with_confirmed_date_key_updates_same_source_record tests/bank_statement_ingestion/test_import_files.py::ImportTests::test_excess_precision_is_not_rounded_and_clear_rows_still_save tests/bank_statement_ingestion/test_bank_history.py::HistoryTests::test_amount_evidence_requires_the_complete_token_and_sign tests/bank_statement_ingestion/test_bank_history.py::HistoryTests::test_currency_separation_and_unknown_values tests/bank_statement_ingestion/test_bank_history.py::HistoryTests::test_excel_date_keys_and_unknown_keys_are_checked_without_reader tests/bank_statement_ingestion/test_distribution.py::DistributionTests::test_installed_copy_creates_and_reads_history_without_network -q
```

Result: 8 passed, 18 subtests passed.

Full focused command:

```sh
python3 -m pytest tests/bank_statement_ingestion/test_import_files.py tests/bank_statement_ingestion/test_bank_history.py tests/bank_statement_ingestion/test_maintenance.py tests/bank_statement_ingestion/test_distribution.py -q
```

Result: 128 passed, 10 failed, 124 subtests passed. Every failure requires the existing XLSX reader dependency `defusedxml==0.7.1`, which is not installed. No package was installed. `python3 -m compileall -q` passed for all changed Python files. `ruff check` could not run because Ruff is not installed.

| Changed file | SHA-256 after edits |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `aba6842fe7a8d971c1468a031c5ffe91f43e8e501238a084ada591c143ac1eec` |
| `skills/bank-statement-ingestion/SKILL.md` | `f0db93905fb96e8844e093592cbce64416d4c8bd5e323a9849cd61e3be66e6a6` |
| `tests/bank_statement_ingestion/test_import_files.py` | `48b282e41388bfd8eb55c2af0aa2f6f725ee5af8f25e7553bcb9f86f2a900586` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `4cb6e7368d17d81086319b0d9b579471c977585248932f4da3686f4639af408e` |
| `tests/bank_statement_ingestion/test_maintenance.py` | `f01a87a657a848bf8698625b626b9a556e1113a4d1b9b77fe2eaf47c45fb4c9a` |
| `tests/bank_statement_ingestion/test_distribution.py` | `1806b6a3c7c89ef62adb571dcec05a3d7901803c5dfc7499b6f59f590d3d1dec` |

## Limits

- Approved files: `bank_history.py`, ingestion `SKILL.md`, `test_import_files.py`, `test_bank_history.py`, `test_maintenance.py` only if required, and `test_distribution.py`.
- Keep `statement_reader.py` unchanged if protected raw fragments and locations suffice.
- No database format change, installer change, package install, real history or live statement.

## Final bounded repair checkpoint

The approved follow-up is complete. Failed conversions now clear any supplied normalized date or amount. Ambiguous slash dates need one checked order source: a format heading in the same date column, a clear date in the same date column, or a clear user answer. The script checks the evidence against the source when possible. It saves this evidence in the existing source-linked record. It keeps retry identity when the user later supplies the evidence. The reader and database format remain unchanged.

The added regression tests cover same-column heading evidence, same-column peer-date evidence, a clear user answer, a conflicting user answer, and invalid conversions with caller-supplied normalized values. Existing invalid-date test now expects no normalized date.

## Prepared-reader test finding before fixture edit

The Coordinator used the existing prepared environment at `/tmp/bank-step2-reader-env`, which already has `defusedxml==0.7.1`; no install was needed. A four-file run with `pytest` available through `/usr/lib/python3/dist-packages` passed 141 tests and 125 subtests, with one failure: `test_text_date_roles_and_distinct_matching_date_cells` adds a posting date to an older fixture but does not add that date's raw text and format key, as the new contract requires. Update only that fixture to supply the original date and `ymd_dash` key for `posting_date`, then rerun. The Coordinator acknowledges this bounded test-data repair before edits.

Focused regression command:

```sh
python3 -m pytest tests/bank_statement_ingestion/test_import_files.py -k 'ambiguous_date or failed_conversion' -q
```

Result after fixture repair: 5 passed, 26 deselected, 3 subtests passed.

Import test command:

```sh
python3 -m pytest tests/bank_statement_ingestion/test_import_files.py -q
```

Result: 22 passed, 10 failed, 12 subtests passed. All 10 failures need the missing XLSX dependency `defusedxml==0.7.1`.

Full four-file command:

```sh
python3 -m pytest tests/bank_statement_ingestion/test_import_files.py tests/bank_statement_ingestion/test_bank_history.py tests/bank_statement_ingestion/test_maintenance.py tests/bank_statement_ingestion/test_distribution.py -q
```

Result: 133 passed, 10 failed, 124 subtests passed. All 10 failures stop because `defusedxml==0.7.1` is not installed. No package was installed.

Compile command:

```sh
python3 -m compileall -q skills/bank-statement-ingestion/scripts/bank_history.py tests/bank_statement_ingestion/test_import_files.py tests/bank_statement_ingestion/test_bank_history.py
```

Result: passed. Whitespace check used a Python `Path.read_text().splitlines()` check for trailing spaces and tabs. Result: none found. Git diff checks were not run because the developer instructions prohibit Git commands. Ruff remains unavailable (`ruff: command not found`).

| Changed file | SHA-256 after this repair |
|---|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | `3e550293bbbb12659f9f6e373a172d7e0cf409c42c5223b1ef4c437f72f9d1d7` |
| `skills/bank-statement-ingestion/SKILL.md` | `938035ee02a55747974b055f3c090313301b17bf3616410c5e83c21bc3305f63` |
| `tests/bank_statement_ingestion/test_import_files.py` | `bfa915d23d92abc4c98a693b2594402a0b3f3706bb4bd408e6278edc33de6d1e` |
| `tests/bank_statement_ingestion/test_bank_history.py` | `a601c5983a40d24316366ae434def7218e10875aa9bd7c8d44340000b85bad65` |

## Prepared-environment fixture repair

The Coordinator found that `test_text_date_roles_and_distinct_matching_date_cells` added a posting date without its source text and key. I updated only this fixture. The CSV case now supplies both raw date fields and `ymd_dash` keys. The XLSX case now uses ISO text in both separate date cells, then supplies the raw text and `ymd_dash` key for both fields. The source text and keys now agree.

Affected test command:

```sh
PYTHONPATH=/usr/lib/python3/dist-packages /tmp/bank-step2-reader-env/bin/python -m pytest tests/bank_statement_ingestion/test_import_files.py::ImportTests::test_text_date_roles_and_distinct_matching_date_cells -q
```

Result: 1 passed.

Full four-file command in the prepared environment:

```sh
PYTHONPATH=/usr/lib/python3/dist-packages /tmp/bank-step2-reader-env/bin/python -m pytest tests/bank_statement_ingestion/test_import_files.py tests/bank_statement_ingestion/test_bank_history.py tests/bank_statement_ingestion/test_maintenance.py tests/bank_statement_ingestion/test_distribution.py -q
```

Result: 142 passed, 125 subtests passed. No installs were made.

| File changed in this repair | SHA-256 after edit |
|---|---|
| `tests/bank_statement_ingestion/test_import_files.py` | `e7262956353d20159d19dc5c4de2952f8dd50f0cd0bc7fea43876f14c49b468f` |
