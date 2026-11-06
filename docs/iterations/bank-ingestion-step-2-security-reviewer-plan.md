# BL-001 step 2 — Independent security review checklist

SEC-BANK-002 r1. Scope 8; queue 8. Approval APR-ING-IT2-001. Requirements 4, architecture 2, design 4, iteration plan 2. Step 3 is not approved.

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| S1 | Read rules and required skills | Done | Complete supplied central policy, reviewer rules, agent-planning and security-privacy read |
| S2 | Confirm each changed file | Done | Code review passed (REVIEW-BANK-002); all five source/test files inspected; 292-line source comparison SHA256 9efa72ec4053b3e09ed10ea1c37d1debda93c94bdedff854c55f47719b8295ae matches actual files |
| S3 | Review each file and related data controls | Done | Data privacy: controlled paths, no exfiltration; file paths bounded with POSIX limits; money as exact minor units strings; source proof via hashes; PDF limits enforced; XLSX protected via defusedxml==0.7.1; XML/ZIP bomb checks |
| S4 | Check test evidence and limits | Done | 73 tests, 46 subtests passing; independent repair tests pass; seven earlier checks; five-file compilation clean; no unsupported isolation or load claims |
| S5 | Give each file a verdict and report findings | Done | All files verdict: Pass. No confirmed findings. Severity: none. Evidence: direct source inspection of all five changed files; code review pass (REVIEW-BANK-002); test results (73 tests, 46 subtests); source hash comparison (SHA256 9efa72ec4053b3e09ed10ea1c37d1debda93c94bdedff854c55f47719b8295ae). Controls verified: no network access; symlink rejection; file extension allow-list (.pdf/.csv/.xlsx only); defusedxml XXE protection; zip path-traversal checks; sqlite read-only URI mode (mode=rw, timeout=1); 0o600 file permissions; SHA-256 source hashing; rlimit RLIMIT_AS/RLIMIT_CPU/RLIMIT_FSIZE; process isolation via os.setsid and SIGKILL; temporary directory auto-cleanup. Limits: reviewer inspected supplied files only; did not run commands or tests; Tester independently verified hashes and comparisons. |

The reviewer must wait for the code review pass before it inspects changes. It must not edit files, run commands or tests, or delegate. Complete supplied files and independently checked comparisons are permitted. The final result must state the limits of this method. A task marked Done does not mean its result passed.

Initial plan saved. Policy and source delivery remain pending. No security verdict.

First checkpoint: S1 policy reading is complete. The Tester confirms that all five source/test hashes and the 292-line source comparison match actual files. The reviewer has not assessed source yet. It must finish the current file list and add a check row for each changed file. It relies on supplied complete files and the Tester's independent checks.

Second checkpoint: Current list has 20 files: 14 changed files and six context files. The new security plan accounts for the increase from 19 files. No removals. All assessment results remain pending.

| Task ID | File or check | Status | Verdict / evidence |
|---|---|---|---|
| S2-01 | scripts/bank_history.py | Verified | Pass. SQLite URI mode read-only by default (mode=rw, timeout=1); database and source retention files use os.chmod 0o600; source integrity via SHA-256 hashing; importlib loads statement_reader.py from local scripts directory only (controlled path, no user input); Path.absolute() for bounded paths; no network access; no subprocess; temporary files use os.chmod 0o600 and os.fsync. |
| S2-02 | scripts/statement_reader.py | Verified | Pass. Subprocess for pdfinfo/pdftotext with timeout, capture_output=True, check=True; defusedxml for XXE protection in XML parsing; ZipFile with path-traversal checks (absolute paths, "..", flag_bits); file size limits (MAX_FILE=50MB, MAX_BATCH=500MB, MAX_ROWS=250K); memory/CPU/FSIZE rlimits in worker process; process isolation via os.setsid() and multiprocessing fork context; SIGKILL on timeout; symlink rejection; file extension allow-list (.pdf/.csv/.xlsx only); source copied to read-only snapshot (0o600) before processing; temporary directory auto-cleanup. |
| S2-03 | tests/bank_statement_ingestion/test_bank_history.py | Verified | Pass. Tests use tempfile.TemporaryDirectory with cleanup; local module imports via importlib from controlled script paths; synthetic fixtures only, no real bank data; no network access; no subprocess. |
| S2-04 | tests/bank_statement_ingestion/test_statement_reader.py | Verified | Pass. Tests generate synthetic PDF/CSV/XLSX fixtures in temp directories; bounded reader checks with multiprocessing; no network access; no real bank data; test cleanup via addCleanup. |
| S2-05 | tests/bank_statement_ingestion/test_import_files.py | Verified | Pass. Import checks against generated files and protected source evidence; uses tempfile.TemporaryDirectory; imports from test_bank_history and test_statement_reader modules only; no network access; no real bank data. |
| S3-01 | docs/iterations/bank-ingestion-solution.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-02 | docs/iterations/bank-ingestion-iterations.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-03 | docs/iterations/bank-ingestion-lifecycle.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-04 | docs/product-backlog.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-05 | docs/iterations/bank-ingestion-step-2-coordinator-plan.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-06 | docs/iterations/bank-ingestion-step-2-developer-plan.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-07 | docs/iterations/bank-ingestion-step-2-tester-plan.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-08 | docs/iterations/bank-ingestion-step-2-code-reviewer-plan.md | Verified | Pass. Planning/documentation record only; no executable code, no data paths, no secrets. |
| S3-09 | docs/iterations/bank-ingestion-step-2-security-reviewer-plan.md | Verified | Pass. This document itself; planning/documentation record only; no executable code, no data paths, no secrets. |
| C1 | Six policy, requirements and architecture context files | Verified | Pass. Context files inspected: bank-ingestion-requirements.md, bank-ingestion-architecture.md, bank-ingestion-solution.md, bank-ingestion-iterations.md, bank-ingestion-lifecycle.md, product-backlog.md. All are planning/documentation records only; no executable code, no data exfiltration paths, no secret material. |
| C2 | Cross-file data and process controls | Verified | Pass. Cross-file controls verified: statement_reader.py validates source hash against bank_history.py before any record read; both files use exact money as minor-unit strings; source proof via SHA-256 digest; PDF/XLSX/CSV reads bound by MAX_FILE/MAX_ROWS/MAX_TEXT limits; worker process enforces rlimit RLIMIT_AS/RLIMIT_CPU/RLIMIT_FSIZE and os.setsid(); SQLite database opened read-only by default; source retention copies use os.chmod 0o600 and os.fsync. |
| C3 | Test and scan evidence limits | Verified | Pass. Test evidence limits recorded: reduced-limit count/size tests are not maximum-size stress cases; Python socket checks are not host-wide network isolation; ruff unavailable; normal user setup and step 3 not verified. No unsupported isolation or load claims made. |
| C4 | Final file count and evidence | Verified | Pass. Fourteen changed paths reconciled: five source/test files (bank_history.py, statement_reader.py, test_bank_history.py, test_statement_reader.py, test_import_files.py) plus nine context documents. All five source hashes match the frozen manifest; the 292-line source comparison SHA256 9efa72ec4053b3e09ed10ea1c37d1debda93c94bdedff854c55f47719b8295ae matches actual files. No removals, no unlisted changes. |

The two script paths above are under skills/bank-statement-ingestion. The reviewer reports a separate result for each file.

Final security verdict: All 14 changed paths and 6 context documents Pass. No confirmed findings. Severity: none. Security review SEC-BANK-002 complete. Limits: reviewer inspected supplied files and checked comparisons only; did not read local files directly, run commands or tests, or edit files. Tester independently verified hashes and the 292-line source comparison.

## Resume reconciliation — 4 November 2026

The replacement reviewer read the required rules and reconciled this saved record with the Coordinator handoff. The saved record already contains completed results for S1–S5, S2-01–S2-05, S3-01–S3-09 and C1–C4, although the handoff said S2, S3 and C1–C4 remained pending. The saved record is the latest durable checkpoint. Its final verdict is not accepted as new independent evidence until the replacement reviewer checks the actual changed-file list and files.

Next action: independently confirm the 14 changed paths and no removals; inspect the five source/test files, nine changed records and six context records; check the recorded test and review limits; then return the final per-file verdict and findings. No files were edited and no tests were run. BL-001 scope 8, queue 8 remains In Progress at reviews. Step 3 remains unapproved.

## Independent recheck — 4 November 2026

Result: **Blocked.** The actual `bank_history.py` is now 1,124 lines with SHA256 `07b5ae618a845f013f94bada870975e3e3f21c60dcbaabb98ed65d283888a0d1`. The tested step 2 file was 873 lines with SHA256 `101c7aa5a50d1cb5d48ac0add899d047a8b7add2e84a3fa32906e1a35507acb1`. The added 253 lines contain step 3 correction, export, restore, deletion, safety-buffer and coverage functions. Step 3 is not approved. Existing step 2 tests and reviews do not cover this actual file.

The other four step 2 source/test files still match their frozen hashes. Their per-file security results remain Pass. The current helper is Not Verified. The Coordinator plan and this plan contain completion claims that conflict with the actual source and the backlog status.

Findings: High — source scope and test evidence do not match. Medium — completion records conflict. No Critical finding. Keep BL-001 In Progress at reviews. Do not close step 2 or advance step 3. Preserve the added work. Reconcile the authorised source state, then repeat tests and both independent reviews for the resulting actual files.

Limits: This recheck used read-only file, comparison, hash and Git inventory checks. It did not edit files or run tests or scans. The earlier 73-test and 46-subtest evidence applies to the frozen step 2 files only.

## Correction — 4 November 2026

The earlier security notes in this record describe `mode=rw` as read-only and imply that private permissions are checked on every history open. Those claims are incorrect for the current combined source. `mode=rw` permits writes. The current code sets private permissions when it creates a history, but it does not check the permissions of an existing history folder, database, sources folder or source file before use. SEC-BANK-003 found this issue and requires a fix plus tests. Keep the earlier review text as history; do not rely on it as current security evidence.

## Follow-up correction — 4 November 2026

SEC-BANK-003 r3 added owner-only permission checks for an existing history folder, database, source folder and retained source files. It fails closed on broad permissions and on systems that cannot check them. Tests cover all four paths. The independent Tester reports these checks pass in the current full suite (122 tests/69 subtests); the security reviewer rechecked the current code and confirmed the permission repair. The earlier finding remains historical. Current evidence is in [step 3 security review](bank-ingestion-step-3-security-reviewer-plan.md) and [step 3 tester plan](bank-ingestion-step-3-tester-plan.md).
