# BL-001 step 2 — Developer checklist

DEV-BANK-002 r1. Scope 8; queue 8. Approval APR-ING-IT2-001. Requirements 4, architecture 2, design 4 and iteration plan 2 apply. Step 3 is unapproved.

| Task ID | Deliverable | Action | Status | Evidence / next action |
|---|---|---|---|---|
| S2-D1 | Rules and actual baseline | Read approved inputs, skills, files, Python/uv/libraries and document guidance/licences | Done | Step 1 hashes match; Python/uv/pdftotext/pytest available; Python reading/protection libraries absent |
| S2-D2 | Two permitted scripts | Add protected readers and connect evidence to history checks | Done | Protected reader, real source binding, cells/signs/dates and header-first coverage checks implemented |
| S2-D3 | Three permitted test paths | Generate synthetic PDF/CSV/XLSX files and check reads/imports/limits/failures | Done | 70 tests and 46 subtests pass in prepared environment |
| S2-D4 | Verification and handoff | Run focused regressions/import checks; report exact inventory, hashes and limits | Done | Seven earlier independent probes pass unchanged; five files compile; baseline/diff/manifest supplied |

Five-path inventory is in bank-ingestion-step-2-coordinator-plan.md. Step 1 source/test baseline hashes: 90a3fb3266cdb319b1269bb05047b78b29835ca7f884c1bf8aebbefe897254f1 and d8c97c8224bce93f7ae5f00d7a218aa7bc937a435d16f50f3084fdfabb029677. Developer owns those paths, preserves unrelated work and makes no planning-record changes. No silent software downloads or user configuration changes. Save baseline findings before implementation.

Baseline: Python 3.14.4, uv 0.12.21, pdftotext 26.01.0, pytest 9.0.2 available. ruff/qpdf and Python pdfplumber/pypdf/openpyxl/defusedxml/reportlab absent. Existing document guidance/licences read in place; no copying. No edits or installations. Reader output must bind quotations/locations to selected source bytes; header/coverage checks precede full row reading. Need concrete explicit library setup choice before dependent reader tests. CSV and missing-software paths can proceed independently once authorised.

Saved setup decision: architecture's package names are proposals, not mandatory. Use installed pdfinfo/pdftotext for text PDFs, built-in CSV/ZIP support and defusedxml for protected read-only XLSX cell extraction. This keeps the approved boundaries and exact numeric cell text; no spreadsheet calculation/formatting engine. pdfinfo available (reported 26.05.0). Candidate pin defusedxml==0.7.1 verified on official PyPI; actual compatibility/protection tests still required. Coordinator treats approved step 2 implementation/tests as authorisation for this necessary temporary development setup and announced it to the user before downloads. Use a new /tmp environment/cache and existing Python; no Python download, user/project configuration or normal installation. Missing protection must return unsupported, with no unsafe fallback. Runtime import/reading never installs software or uses the network. No source changes before this saved acknowledgement.

Setup progress: /tmp/bank-step2-reader-env and /tmp/bank-step2-uv-cache created. Initial sandbox DNS failed; authorised native escalation succeeded. defusedxml 0.7.1 metadata/import and safe XML parsing verified; DTD/entity input rejected with protections enabled. No user/project setup changed. Reader dependencies remain lazy. History check/save will invoke protected reading directly rather than accept a caller-created reader result; real locations/quotations and header classification checked. Unknown layouts ask for user dates. Reader and synthetic tests in progress; no complete reader/import result claimed yet.

First runnable checkpoint: 41 existing history tests pass with protected source reads. Tests use real row locations; incorrect shifted locations on unchanged source bytes stop. Reader draft uses lazy protection imports, private snapshots, bounded child processes, ZIP/XML checks and installed PDF tools. Record inputs identify amount cells and source/user sign evidence; raw positive amounts remain distinct from accepted signed amounts. Actual PDF/XLSX fixtures and limit checks still in progress. This is Developer evidence, not independent completion.

Focused progress: 65 tests pass in the prepared environment, including generated PDF/XLSX, ZIP/XML attacks, missing protection, child time/memory failure, network-disabled reads, Debit/Credit cells, forged source evidence, header-first stopping and a temporary installed copy. Sign-answer retry remains under check. Draft preserves Excel serial/scientific raw text as unresolved; Coordinator requested a minimal exact conversion for unambiguous standard date styles/epochs and bounded scientific money if feasible within the same functions. Unknown styles/fictitious dates/unsafe exponents must stay unresolved. No extra components or scope; final test results pending.

Final focused progress: built-in XLSX date styles 14–17/22 with 1900/1904 epochs now return checked canonical dates separately from raw serials; unknown styles, unsupported mappings and fictitious 1900-02-29 remain unresolved. Decimal/scientific money uses bounded exact digit/power-of-ten conversion, no floats. Prepared environment reports 69 tests and 46 subtests pass, including date-cell evidence and sign-answer retry retaining one original record. All five files compile. Final inventory/hashes/diff and earlier independent-probe compatibility checks remain before handoff. No extra scope.

## Final Developer handoff

Prepared-environment command: PYTHONPATH=/usr/lib/python3/dist-packages /tmp/bank-step2-reader-env/bin/python -m pytest -q tests/bank_statement_ingestion. Result: 70 passed, 46 subtests passed. Both earlier independent probe files pass all seven checks unchanged; all five files compile. Final check prevents a transaction-date cell from also proving an absent posting date. A system-Python run failed the isolated XLSX check because its protection library is absent; prepared Python passed. ruff unavailable; unrelated tests and step 3 not run.

| File | Lines | SHA256 |
|---|---:|---|
| skills/bank-statement-ingestion/scripts/bank_history.py | 849 | aec7feeb6af03cfd3588266830488539d4af6a834c082f120908f48133eff7cc |
| skills/bank-statement-ingestion/scripts/statement_reader.py | 305 | 05588dd5eea9b3db64c41b03dcf0a1b86b87afa22672fb7e41107b41484094f5 |
| tests/bank_statement_ingestion/test_bank_history.py | 484 | aa74b3b10731edd0f92e4c7d5499152e45ba69fce5c55c431c77e735d03b4d9c |
| tests/bank_statement_ingestion/test_statement_reader.py | 190 | 68d45072e53aab01c8a9aa2e7fe880d799322fa16910136a951df70ece1f4c48 |
| tests/bank_statement_ingestion/test_import_files.py | 272 | 98fc9077d361f07aa8eee519066a3711bf488e5a3f2a1f8980eae58a41461520 |

Actual artifacts: /tmp/bank-step2-baseline; /tmp/bank_step2_full.diff (1,044 lines, including three complete new files); /tmp/bank_step2_manifest.json. No documentation or other repository edits by Developer. Unknown layouts/custom date styles remain unresolved/unsupported. Process protection currently requires POSIX; unsupported hosts fail before reading. These limits must appear in later skill instructions. Independent tests/code/security reviews remain required; no finished-skill claim.

## DEV-BANK-002 r2 — independent date-role failure

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| F1 | Check date proof against source column meaning | Done | Linked numeric and structured text dates checked against actual column roles |
| F2 | Prevent unsupported reuse of one cell for two date fields | Done | One cell cannot supply two roles; distinct valid cells preserved |
| F3 | Add both regressions, rerun independent cases/suite and return hashes/diff | Done | 73 tests/46 subtests; three new probes and earlier seven pass; all five files compile |

Repair scope remains five approved source/test paths. Preserve valid partial records and accepted values; uncertain interpretations must not establish false coverage. No new model/framework or later-step work. Save this checklist before repair edits.

Developer r2 handoff: repair changed only bank_history.py (873 lines, SHA256 101c7aa5a50d1cb5d48ac0add899d047a8b7add2e84a3fa32906e1a35507acb1) and test_import_files.py (303 lines, SHA256 26a94c62537a0e45141b5981918072f5f96418fb9c9c791236d36f392255a830). Other three hashes unchanged. Complete scoped diff now /tmp/bank_step2_full.diff (1,099 lines); exact repair diff /tmp/bank_step2_r2.diff (90 lines), pre-repair files /tmp/bank-step2-r2-before; manifest includes original/pre-repair/final hashes. No other edits/setup changes. ruff unavailable; no host-network-isolation claim. Independent retest pending.

## Read-only code-review artifact handoff

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| A1 | Check frozen hashes and captured source/document baselines | Done | Actual frozen files checked |
| A2 | Send full source/test and required policy/approved texts | Done | Five complete files and two policies supplied |
| A3 | Send full real document diffs and new plans | Done | Complete 292-line existing-source comparison supplied; Tester owns document comparisons |
| A4 | Return complete manifest/delivery coverage and gaps | Done | Seven assigned artifacts delivered; no source changes |

Coordinator saved this specialist plan before artifact reading. Frozen independent retest passed. Reviewer lacks a permitted native reader and accepts complete supplied artifacts; Tester must independently verify actual hashes/comparisons. Current step 2 modified/new records are reviewed, not unrelated source changes or untouched historical plans.

Final artifact handoff: Five complete source/test files and code-review/code-simplification policies supplied. All chunks cover their full line ranges. Existing-source comparison: 292 lines, SHA256 `9efa72ec4053b3e09ed10ea1c37d1debda93c94bdedff854c55f47719b8295ae`; Tester independently checked it against actual before/current files. The three new files were supplied in full. No source edits, setup or new tests in this batch.

## SEC-SUPPLY-BANK-002 r1 — read-only security artifacts

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| S1 | Check frozen source hashes and read two security policies | Pending | No file changes or tests |
| S2 | Supply complete five source/test files and both security policies | Pending | Paths, hashes, line counts and complete labelled chunks |
| S3 | Supply the complete checked source comparison | Pending | True before/after hashes; three new file bodies supplied separately |
| S4 | Report delivery coverage and gaps | Pending | Keep Tester records; no review verdict or project edits |

Initial plan saved. Developer must wait for acknowledgement before this batch. Tester owns current policy/core/administrative records and independent checks.
