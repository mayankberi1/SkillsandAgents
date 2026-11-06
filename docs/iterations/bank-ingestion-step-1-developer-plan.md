# BL-001 step 1 — Developer checklist

Assignment DEV-BANK-001 r1. Scope 8; queue 8. Stage implementation. Approval APR-ING-IT1-001 covers step 1 only. Approved inputs: requirements 4, architecture 2, design 3 with user-requested design 4 packaging update, iteration plan 2.

| Task ID | File / deliverable | Action | Status | Evidence | Next action |
|---|---|---|---|---|---|
| D1 | Approved inputs and actual baseline | Inspect rules, skills and files; return evidence before edits | Done | Read approved inputs, AGENTS, implementation/planning skills and file baseline; no existing bank module/root tests | Coordinator acknowledged baseline |
| D2 | skills/bank-statement-ingestion/scripts/bank_history.py | Implement approved standard-library history and import checks | Done | New 712-line helper; eight tables and direct functions | Independent reviews |
| D3 | tests/bank_statement_ingestion/test_bank_history.py | Test money, scope, periods, overlap, sources and safe retries | Done | New 394-line synthetic test file; ING-010-A–N and failure cases | Independent tester |
| D4 | Verification and handoff | Run focused checks and report actual inventory/coverage/limits | Done | Python 3.14.4: 33 tests and 7 subtests pass; both files compile | ruff unavailable; independent checks required |

Developer owns the two permitted source/test paths and must preserve unrelated work. No installer, reader, SKILL.md, external library or maintenance implementation. Coordinator alone persists planning records. Save the baseline checkpoint before permitting implementation.

Baseline checkpoint: system Python 3.14.4 satisfies >=3.13; do not use the old 3.12 .venv. pytest available, ruff absent from PATH. No existing callers, config or exports. Proposed eight-table implementation uses explicit typed inputs, retained source verification before per-file SQLite saves, and range checks under BEGIN IMMEDIATE. check_statement will use the same checks without saving. No material conflict, file edits or tests at baseline. D2–D4 may proceed after saved acknowledgement; report lint limitation without installing software silently.

Progress checkpoint: Developer reports 24 focused tests passing on Python 3.14.4. The first run exposed synthetic fixtures that reused identical bytes across different source/account cases; fixtures corrected without weakening identity checks. Missing/changed retained copies block import and preserve history; partial retries preserve two identical purchases. Balance reconciliation, durable failed-attempt visibility and boundary cases remain in progress. Draft production module about 650 lines; independent simplification review required. ruff remains unavailable. This is not a completion or independent verification result.

Final developer checkpoint: 33 tests and 7 money subtests pass; both files compile. Public functions: minor_units, create_history, save_account, save_card, save_period_note, check_statement, save_statement, read_history. Durable failed-attempt records, balance differences, unsupported credit sign basis, ambiguous dates and wrong card-section assignments checked. Standard library only, inline declarations. No unrelated changes. Readers and correction/export/restore/deletion remain outside step 1. Source quotations still rely on caller evidence until step 2. Long SQL and section-import complexity require independent review. Feature is not complete or installed.

## DEV-BANK-001 r2 — independent test fixes

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| F1 | Match complete amount and sign evidence | Done | Complete numeric tokens and exact signs required |
| F2 | Enforce actual boolean inputs before financial changes | Done | complete, reliable_reference, expected and withdraw require booleans |
| F3 | Match complete valid header dates | Done | Complete date evidence required |
| F4 | Retain valid work when a record date is invalid | Done | Invalid dates unresolved; valid records save without verified coverage |
| F5 | Add regression tests and rerun existing plus independent checks | Done | 37 tests and 21 subtests pass; all four independent repros report OK; both files compile |

Scope remains the same two approved source/test files. Coordinator corrected stale design state. No changes to approved behaviour or later steps. Save and acknowledge this checklist before remediation.

Developer r2 handoff: F1–F5 fixed in the same two files; no new files/framework/design changes. All four independent reproduction results inspected rather than relying on exit status. ruff unavailable. Independent tester must recheck before failure status clears.

## DEV-BANK-001 r3 — review reproductions

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| P1 | Reproduce account currency/precision change with saved targets | Done | AUD precision2 target100.00/buffer20.00 become 10000/2000 under JPY precision0 |
| P2 | Reproduce exact-repeat effect on reconciliation | Done | Exact retry changes imported outcome; matched reconciliation becomes unavailable |
| P3 | Reproduce reliable-reference date conflict in covered overlap | Done | Changed REF1 date silently ignored; February coverage completes with no question |

Reviewer candidates received. Source and tests remain frozen while artifact review continues. Reproduction only is authorised in this batch; save results before any repair edits.

Saved reproduction checkpoint: P1 and P2 confirmed without source edits. Proposed minimal fixes: require explicit replacement/clear of existing money settings for unit changes; preserve completed statement outcome and put retry outcome in changes. P3 is a new related reviewer candidate to reproduce before repair scope is finalised.

## DEV-BANK-001 r4 — code review fixes

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| G1 | Prevent reinterpretation of existing money settings on unit changes | Done | Existing settings must explicitly be replaced or cleared |
| G2 | Preserve completed statement metadata on repeat upload | Done | Retry result recorded without overwriting completed statement |
| G3 | Use one reliable-reference comparison in covered/uncovered paths | Done | Common field comparison; conflicts unresolved with accepted values retained |
| G4 | Add focused regressions, run suite/reproductions and return exact diff | Done | 41 tests/27 subtests; original four and new three probes pass; compile passes; 114-line full diff |

Source-only review of the frozen base completed. Coordinator authorises repairs for three reproduced defects only; the reviewed base remains identified by hash. Reviewer must inspect the exact resulting diff before passing. No new model, tables, reader or later-step work.

Developer r4 handoff: complete before files in /tmp/bank_history_r4_before.py and /tmp/test_bank_history_r4_before.py; full unified diff /tmp/bank_step1_r4_full.diff. Production SHA256 ebbde4654497534e02b602de0537b567ffc6a5bbb8b37c4d38f5bdf0645b3673 → 90a3fb3266cdb319b1269bb05047b78b29835ca7f884c1bf8aebbefe897254f1. Tests SHA256 f5f4045318fa4a494602b9290dcdeb5f60c88dd99867d3766b0a31b288379b3c → d8c97c8224bce93f7ae5f00d7a218aa7bc937a435d16f50f3084fdfabb029677. New fixture-byte reuse corrected without weakening source identity. ruff unavailable. Independent retest and exact diff review still required.

## Read-only security artifact handoff

Security Reviewer also lacks a permitted native file reader and accepts complete supplied artifacts. Developer may supply current full actual source/test files, policy/approved-input files and changed planning records directly to /root/security_reviewer, with hashes, line counts and bounded complete chunks. No review delegation, source edits, execution changes or summaries as substitutes. Report a complete manifest and delivery limitations; independent Tester checks source hashes separately.
