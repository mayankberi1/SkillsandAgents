# BL-001 step 2 — Coordinator checklist

Assignment COORD-BANK-002 r1. Scope 8; queue 8. Approval APR-ING-IT2-001, user “yes”. Inputs: requirements 4, architecture 2, design 4 and iteration plan 2. Step 1 complete; step 3 unapproved.

| Task ID | Action | Status | Evidence / next action |
|---|---|---|---|
| C1 | Record approval and current feature state | Done | Iteration record and backlog updated |
| C2 | Save developer initial and baseline checkpoints | Done | Baseline and minimal temporary setup decision saved/announced; source hashes match step 1 |
| C3 | Reconcile scoped implementation and tests | Done | Five-path handoff saved; 70 tests/46 subtests, seven earlier probes and compilation reported passing |
| C4 | Save independent testing and reviews | Blocked | Frozen step 2 tests and code review passed. The 4 November security recheck found that actual `bank_history.py` now includes 253 unapproved step 3 lines and no longer matches the tested hash. Repeat tests and reviews after source/scope reconciliation. |
| C5 | Record step completion and next approval | Done | User approved step 3 under APR-ING-IT3-001 on 4 November 2026. Step 2 frozen evidence does not cover the current combined source; step 3 must include full tests and independent reviews before completion. |

Allowed source/test files: skills/bank-statement-ingestion/scripts/bank_history.py; skills/bank-statement-ingestion/scripts/statement_reader.py; tests/bank_statement_ingestion/test_bank_history.py; tests/bank_statement_ingestion/test_statement_reader.py; tests/bank_statement_ingestion/test_import_files.py. No requirements.txt, SKILL.md, installers, project dependency/lock files or normal user configuration changes. Keep retained approval/failure history. Coordinator owns planning records; Developer owns implementation.

Inspect installed tools/libraries and source evidence before selecting library versions. Setup must be explicit; statement reads and module imports must not download software or use the network. No real bank data. Keep runtime limits and exact money checks. Reuse existing document-reading guidance in place without copying licensed material.

Baseline decision: use existing PDF tools plus only defusedxml for protected XLSX extraction; architecture's package list is non-mandatory. Development-only /tmp environment/cache setup is necessary for approved implementation/tests; announced before download. No normal user installation or project dependency changes. Candidate defusedxml 0.7.1 checked on official PyPI (https://pypi.org/project/defusedxml/); not claimed tested until actual checks. No requirement/architecture scope change.
