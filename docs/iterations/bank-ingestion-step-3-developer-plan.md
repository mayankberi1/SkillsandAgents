# BL-001 step 3 — Developer checklist

Assignment DEV-BANK-003 r1. Scope 8, queue 8. Approval APR-ING-IT3-001, user request “continue with step 3 development” (4 November 2026). Step 3 scope is corrections, recovery, export/restore/deletion, skill instructions, catalogue updates, and checks for ING-001–014. The source already contains unreviewed step 3 work; preserve it and verify the actual combined result.

| Task ID | File / criterion | Planned action | Status | Result / evidence / next action |
|---|---|---|---|---|
| D1 | Actual source, approved design and step 3 criteria | Inspect current changes and reconcile paths; keep user work | Done | Eight-path baseline recorded; current helper is 1,124 lines; source additions are unreviewed |
| D2 | bank_history.py; test_bank_history.py; test_import_files.py | Complete safe corrections, recovery, export, restore and deletion behavior | In Progress | Gaps: corrections do not save the change; export may overwrite; restore accepts damaged/empty history; deletion can remove live data; coverage rebuild loses source links and mixes card/account periods |
| D3 | test_maintenance.py; test_distribution.py | Add synthetic tests for maintenance and installed-copy use | In Progress | Maintenance tests exist; update incorrect empty-restore expectation; distribution test is absent |
| D4 | SKILL.md; README.md; skills/CATALOG.md | Add final user instructions and catalogue entries; check setup and privacy limits | In Progress | Skill needs checked uv setup instructions and accurate host protection limits |
| D5 | ING-001–014 and actual changed-file inventory | Run scoped checks, report hashes and limits, prepare complete handoff | Pending | Independent testing and reviews remain separate |

Allowed paths: `skills/bank-statement-ingestion/scripts/bank_history.py`, `tests/bank_statement_ingestion/test_bank_history.py`, `tests/bank_statement_ingestion/test_import_files.py`, new `tests/bank_statement_ingestion/test_maintenance.py`, new `tests/bank_statement_ingestion/test_distribution.py`, new `skills/bank-statement-ingestion/SKILL.md`, `README.md`, and `skills/CATALOG.md`. Do not edit installer scripts or add requirements/lock files. Keep real bank data out of tests. Use a temporary installed copy; do not run a skill from source or change normal user configuration.

Initial plan only. Wait for Coordinator acknowledgement before inspecting or editing files. Preserve prior step 2 test/review records and disclose that their hashes do not cover the current combined source.

## D1 baseline checkpoint — before edits or tests

Developer inspected the current source and approved inputs. Actual baseline: `bank_history.py` 1,124 lines, SHA256 `07b5ae618a845f013f94bada870975e3e3f21c60dcbaabb98ed65d283888a0d1`; `test_bank_history.py` 484 lines, SHA256 `aa74b3b10731edd0f92e4c7d5499152e45ba69fce5c55c431c77e735d03b4d9c`; `test_import_files.py` 303 lines, SHA256 `26a94c62537a0e45141b5981918072f5f96418fb9c9c791236d36f392255a830`; `test_maintenance.py` 277 lines, SHA256 `f96a0bcdbc91184f32bb7a48ef2d36186bde944d16122d5857c756541dedcb9e`; `test_distribution.py` is absent; `SKILL.md` 72 lines, SHA256 `d9cd5c60ac4c32d03a6a0f30bf9f41ae9785cb40312621a848e7e1c0dec7a47d`; `README.md` 158 lines, SHA256 `bdd959a18a5b0bdf5e7c92fa2d690604fc1d661e1c41cc2bccd32c1542994ff4`; `skills/CATALOG.md` 22 lines, SHA256 `a156ba77c5b01a44acb85680a2fc8eb742cd8fd999de5ade16b50a1580835a7a`.

No tests or edits in D1. Gaps found: correction changes are not saved; unknown fields may be lost; reports do not show stale data; export may overwrite and include untracked files; restore may accept damaged or empty data and omit the source folder; deletion may remove dependent data or live files; coverage rebuild may mix card/account periods and lose source links. The maintenance test expects an empty restore to pass; distribution test is absent. The skill lacks checked setup commands and describes host process limits as a sandbox. Earlier step 2 tests do not cover this source.

The developer proposes changes within existing functions and paths. Preserve the added functionality while fixing unsafe behavior. Keep safety-buffer work to approved observed-balance checks; projected balance forecasts remain outside this item. No new components or automatic user setup.

## D2–D4 edit plan checkpoint — awaiting acknowledgement

Proposed changed files: all eight paths in scope. Developer will correct existing maintenance functions and add `correct_history` and `delete_history` entry points. Corrections will validate user evidence and selected IDs, preserve original records and stable transaction IDs, save old/new values with a reason, and mark affected reports or coverage out of date. Range replacement will preserve unrelated records and record replacement/recovery choices. Coverage will keep account and card periods separate and retain source links.

Export will create a new private destination with a SQLite backup and only linked, verified source files. Restore will validate the database and source files before writing to a new private directory. Failed work will not reset existing history. Deletion will resolve related records and shared sources, keep external originals, and require explicit whole-history scope before deleting the full data set.

Tests will use synthetic files. They will cover correction history, range replacement, coverage/source links, missing or changed sources, failed export/restore, existing destinations, selected and shared-source deletion, recovery choices, stale reports, and a temporary installed copy. The current empty-database restore test will change to reject invalid history. No normal user setup or new dependencies.

The skill will retain its YAML frontmatter and give concise checked `uv` setup commands, prepared-interpreter use, privacy limits, period checks, retries, and recovery instructions. README/catalogue edits will stay limited to affected entries. Capture all eight path baselines before edits. Do not run tests until the implementation checkpoint is saved. Independent testing and code/security reviews remain separate.

## D2–D4 progress checkpoint

Developer captured the full eight-path baseline and is editing the approved files. Corrections now retain old/new values and invalidate affected coverage. Recovery copies check the database and sources and reject existing destinations. Deletion calculates its effects and checks them again before changing records. Explicit replacement, shared-source handling, skill instructions and synthetic tests remain in progress. No tests or setup have run. Exact changed paths and hashes are due before testing.

## D2–D4 implementation checkpoint — before verification

Developer implemented in six of eight allowed paths; the existing history and import test files are unchanged. Full diff: `/tmp/bank-step3-implementation.diff` (1,176 lines). Baseline and inventory: `/tmp/bank-step3-baseline`, `/tmp/bank-step3-implementation-manifest.json`.

| File | Lines after edit | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,227 | `3e6662b68d46705075e48b790eee7da9f6022cfd389c016fa6642a804a3d9676` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 506 | `2fbc95ad94394ddf5a0f46ef3a776088c314ac65f8e3868847f3e82af11b6ad3` |
| `tests/bank_statement_ingestion/test_distribution.py` | 66 | `79e4950a2f1db4691e2127bb7ac83be13f45f3177e5ce2dc44b4bb8901a173d3` |
| `skills/bank-statement-ingestion/SKILL.md` | 69 | `4788844aace48d9595e0b8b2571a2bc11070b27699b99346abb6073cc3c11da4` |
| `README.md` | 159 | `e72306bcbb9b99cfc9d8079e76a3908fd7aeead105f841c50f5fdf973ca923e1` |
| `skills/CATALOG.md` | 22 | `8c290205f06f8d308e13c7159f0022a2d0a7ae5a267e04cef6c07a0547e5a38d` |

Implemented behavior includes saved correction history with stable IDs, source replacement checks and recovery choices, private export/restore to new folders, selected deletion with shared/external source handling, source/card-specific coverage, and observed-balance checks only. Synthetic tests cover maintenance failures and a temporary installed-copy import/retry. Skill setup and host limits plus affected catalogue text were updated. No tests, compile, lint or setup have run for this state. Coordinator acknowledgement is required before verification. Independent testing and reviews remain separate.

## First focused test checkpoint — repair required

Developer ran the first focused tests: 40 passed and 15 subtests passed; two fixture failures. One shared-source CSV put the second account header after transaction rows, so the header-first reader correctly stopped. One installed-copy network guard replaced `socket.socket` and broke lazy SSL setup before a network call. No product defect was reported. Repair only these test fixtures: place both explicit account headers before rows, and block socket connection attempts without replacing the socket class. No setup or downloads. Save this failure before repair and rerun focused plus full bank checks after repair.

## DEV-BANK-003 r1 final development handoff

Implementation and Developer verification are complete. The two first-run failures were test fixture issues; the saved, narrow repair fixed them.

| Check | Result |
|---|---|
| Focused maintenance and installed-copy tests | 42 passed; 15 subtests passed |
| Full bank statement suite, including actual combined helper | 115 passed; 61 subtests passed |
| Python compilation for helper, reader and five bank test files | Passed |
| Ruff | Unavailable; no lint run |
| External network isolation | Not proven; test blocks socket connections only |

Final SHA256 and line counts:

| File | Lines | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,227 | `3e6662b68d46705075e48b790eee7da9f6022cfd389c016fa6642a804a3d9676` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 506 | `3ea06188e0ec9a6ad4434d84124c97680b24cc6804206ce3029435c7265c0910` |
| `tests/bank_statement_ingestion/test_distribution.py` | 66 | `4427d4912c243d1be5e0816ae2dbcd4d4e97bc2b5e08c1b69247a57d192e146d` |
| `skills/bank-statement-ingestion/SKILL.md` | 69 | `4788844aace48d9595e0b8b2571a2bc11070b27699b99346abb6073cc3c11da4` |
| `README.md` | 159 | `e72306bcbb9b99cfc9d8079e76a3908fd7aeead105f841c50f5fdf973ca923e1` |
| `skills/CATALOG.md` | 22 | `8c290205f06f8d308e13c7159f0022a2d0a7ae5a267e04cef6c07a0547e5a38d` |

Unchanged: `tests/bank_statement_ingestion/test_bank_history.py` SHA256 `aa74b3b10731edd0f92e4c7d5499152e45ba69fce5c55c431c77e735d03b4d9c`; `test_import_files.py` SHA256 `26a94c62537a0e45141b5981918072f5f96418fb9c9c791236d36f392255a830`; statement reader unchanged. Full diff and manifest are recorded in `/tmp/bank-step3-final.diff` and `/tmp/bank-step3-final-manifest.json`; repair diff is `/tmp/bank-step3-fixture-repair.diff`. The Tester and independent code/security reviewers must review the actual current files and changes before BL-001 is complete.

Known limits: Deletion reports source files or backups that remain shared or unselected. File cleanup can fail after database deletion; the result reports retained paths. Coverage keeps statement/card scope and does not infer gaps from transactions. Safety-buffer checks compare observed balances only; no forecast. No new production module, dependency, installer or schema was added.

## DEV-BANK-003 r2 — code review repairs

REVIEW-BANK-003 r1 returned three P2 findings. Before edits, fix and test only these items:

| Task | Required change | Status |
|---|---|---|
| F1 | Keep verified coverage after description/amount-only corrections; invalidate only when source/account/date changes require it; add regression test | Done |
| F2 | On unresolved `correct_history`, remove the copied untracked source or retain it visibly as retry data; add failure-path assertion | Done |
| F3 | Replace repeated transaction-by-record deletion scans with one index or scoped query; preserve preview/recheck behavior | Done |
| F4 | Return exact changed paths, hashes and diff before tests; run focused and full suite/compile after the saved repair checkpoint | Done | Focused 45/15; full suite 118/61; compile passed; hashes unchanged after tests |

Do not change unrelated behavior. Save this repair plan before edits. Security review remains separate.

Developer acknowledged r2 before edits. F1–F3 are limited to coverage invalidation, cleanup/tracking after rollback, and one indexed deletion support lookup. Current repair baseline and exact diff/hash checkpoint are required before tests.

F1–F3 implementation is complete. Focused tests passed: 45 tests and 15 subtests. Full bank suite passed: 118 tests and 61 subtests. Compilation passed for the helper, unchanged reader and all five bank tests. Final hashes match the saved repair checkpoint. No setup/download. Ruff unavailable; no full-scale performance benchmark or host-network isolation claim. Independent retest and code/security review remain.

## DEV-BANK-003 r3 — security repairs

SEC-BANK-003 r1 returned one High/P1 and two P2 findings. Before edits, address only these items:

| Task | Required change | Status |
|---|---|---|
| S-F1 | Validate every stored hash/path before deletion; require a safe hash basename and resolved target inside the managed source folder; add corrupt-database traversal test proving outside file stays | Pending |
| S-F2 | Check existing history folder, database, source folder and source file permissions before use; fail safely on broad permissions or set private permissions; test each open-permission case | Pending |
| S-F3 | Filter account-specific `read_history` source/file and change rows to the selected account; add two-account privacy test | Pending |
| S-F4 | Return exact changed paths, before/after hashes and complete delta before tests; run focused/full suite and compile after saved checkpoint | Pending |

Coordinator also appended a dated correction to the step 2 security record. Keep its earlier inaccurate claims as history. No unrelated changes. Save this repair plan before edits; security re-review remains separate.

Developer acknowledged r3 before edits. S-F1 validates stored hashes and confirms deletion targets stay inside the managed folder. S-F2 rejects broad permissions on existing history/database/source paths. S-F3 filters account-specific source and change output. Tests cover traversal, each of four permission locations, and two-account isolation. Exact diff/hashes are required before tests.

## DEV-BANK-003 r3 repair checkpoint — before tests

Three changed files; the YAML fields in the skill remain unchanged. Baseline: `/tmp/bank-step3-r3-before`. Diff: `/tmp/bank-step3-r3.diff` (161 lines), SHA256 `4108a0d8cdd7984655accba5e72d051c1e89544af71c742a41480984f271d7d9`. Manifest: `/tmp/bank-step3-r3-manifest.json`.

| File | Lines | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,280 | `931598e6aee49e16de2bde8af6c71c2f73efb8808616e5469677f7ad9e174a04` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 601 | `cc77976d047e6bc551999116abf7589d6b03b501a6c46a74dffc6586e6f74ec0` |
| `skills/bank-statement-ingestion/SKILL.md` | 71 | `51d2b1c757c77e3390abaa862edc6e888a0a7cf59f085975f3348120917ba493` |

S-F1 validates every stored source hash/path, rejects symlinks and confirms the resolved deletion target stays in the managed source folder. Corrupt database tests check traversal hash and traversal path while preserving the outside file and history. S-F2 fails closed when the existing history folder, database, source folder or retained source entry has broad permissions. It does not silently change existing modes. Four separate permission cases were added. S-F3 filters account-specific source/file/change results; two-account checks confirm isolation and unfiltered reads retain both. The skill describes these limits. No tests, compile, lint or setup have run after these edits. Coordinator acknowledgement is required before verification. Security re-review remains required.

## DEV-BANK-003 r3 test checkpoint — two fixture failures

Focused security-repair tests passed: 48 tests and 21 subtests; compilation passed. The full suite had 119 tests and 67 subtests pass, with two failures. Both old history fixtures recreated managed files at mode 0644. The new owner-only permission check correctly stopped the tests before they reached their intended missing/changed-source and pending-cleanup cases. Repair only `test_bank_history.py`: set mode 0600 on those synthetic managed files. Preserve the production permission checks and all other assertions. This adds a fourth changed file. No source changes after the saved r3 checkpoint; no setup/download. Save this failure before test-fixture edits and retest the full suite.

## DEV-BANK-003 r3 final handoff

The permission checks are unchanged. Three private-mode adjustments in `test_bank_history.py` let the older synthetic fixtures reach their intended checks. The first full-suite failure remains recorded above.

| Check | Result |
|---|---|
| Focused history/maintenance/distribution tests | 89 passed, 48 subtests |
| Full bank suite | 121 passed, 67 subtests |
| Python compilation | Passed for helper, unchanged reader and all five bank tests |
| Ruff | Unavailable; no lint run |

Final changed-file hashes:

| File | Lines | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,280 | `931598e6aee49e16de2bde8af6c71c2f73efb8808616e5469677f7ad9e174a04` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 601 | `cc77976d047e6bc551999116abf7589d6b03b501a6c46a74dffc6586e6f74ec0` |
| `skills/bank-statement-ingestion/SKILL.md` | 71 | `51d2b1c757c77e3390abaa862edc6e888a0a7cf59f085975f3348120917ba493` |
| `tests/bank_statement_ingestion/test_bank_history.py` | 487 | `27cad6bd5b103ee6fe5c7610538dd31f9225278e3dea3ac06386467c35e5db32` |

The three security fixes add two corrupt-path tests, four permission checks, and two-account output filtering. Permission checks use POSIX modes and fail closed where checks are unsupported. No claim of a host sandbox, network isolation or secure erasure. Diff: `/tmp/bank-step3-r3-final.diff` (185 lines), SHA256 `b880ad13010c7042db87dd4a3dd662cb4c1baccf587d07c7b0143f5c93b15464`; full step 3 comparison: `/tmp/bank-step3-r3-full.diff` (1,389 lines), SHA256 `3d8319ca60ae439ea9e1c34c514b5290aab05231a5bf6de1ec34dea68b8e501e`. Manifest: `/tmp/bank-step3-r3-full-manifest.json`. Independent tester and code/security reviewers must recheck these current files.

## DEV-BANK-003 r4 — account reassignment history

REVIEW-BANK-003 r3 returned one P2. Before editing, fix only this issue: when a correction moves a transaction from account A to B, make the correction visible in both relevant account histories while keeping unrelated account evidence hidden. Add tests for both views after reassignment. No other behavior changes. Save exact changed paths/hashes before tests; rerun focused/full suite and compile. Wait for Coordinator acknowledgement before edits.

Developer acknowledged r4 before edits. Account-filtered changes will remain visible when either the saved old or new account matches the selected account, plus existing record links. Tests will check both affected accounts and an unrelated third account, including a later reassignment. No other output expands.

## DEV-BANK-003 r4 checkpoint — before tests

Two paths changed. Baseline: `/tmp/bank-step3-r4-before`. Diff: `/tmp/bank-step3-r4.diff` (52 lines), SHA256 `b98bffdad5b88b94222151acfd4d8f0bcaa2b7c12c9644dbbc357de7639fd8fd`. Manifest: `/tmp/bank-step3-r4-manifest.json`.

| File | Lines | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,288 | `79e31e57121e4f40b689dca274a17f4b06ff3b1adf6078b03d0d871de1123d31` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 625 | `aa64c69f40edb90541848f847b0e73aec304de4dbfb822df604b999582d32af8` |

Account-scoped correction events are visible when either the saved old or new account matches the view, even after later moves. The regression checks both affected accounts, a third unrelated account, unrelated file/evidence filtering, and event retention after a move back. No tests, compile or setup have run. Coordinator acknowledgement is required before verification.

## DEV-BANK-003 r4 final handoff

Focused maintenance/distribution checks passed: 49 tests and 23 subtests. Full bank suite passed: 122 tests and 69 subtests. Compilation passed for both scripts and all five bank tests. No failures; no setup/download. The two changed hashes match the saved checkpoint. Ruff remains unavailable; unrelated tests and old `/tmp` probes were not rerun. Independent tester, code and security re-review remain required.

Full step 3 comparison: `/tmp/bank-step3-r4-full.diff` (1,421 lines), SHA256 `d1240f01872743fb2fd205dccf9c587509e4b7563c9c3e983b9a1550c8060751`. Full inventory: `/tmp/bank-step3-r4-full-manifest.json`. Exact r4 delta and manifest remain at `/tmp/bank-step3-r4.diff` and `/tmp/bank-step3-r4-manifest.json`.

## DEV-BANK-003 r2 repair checkpoint — before tests

Three files changed. Current repair baseline: `/tmp/bank-step3-r2-before`. Full diff: `/tmp/bank-step3-r2.diff` (216 lines), SHA256 `ff7cf73802dc36f0c35febbf96fcf2c0f4e2ee2cddf04610f4f1771e21ba9b64`. Manifest: `/tmp/bank-step3-r2-manifest.json`.

| File | Lines | SHA256 |
|---|---:|---|
| `skills/bank-statement-ingestion/scripts/bank_history.py` | 1,246 | `8db15b434d57c31ce47e51130b73abc542973af080bf8686bfb4ab16fa368d93` |
| `tests/bank_statement_ingestion/test_maintenance.py` | 551 | `1008093661c4e200ae2047998be55b03ef7519860e82b9651ff786e5fdf799a5` |
| `skills/bank-statement-ingestion/SKILL.md` | 69 | `eae5ed373ee9333e6704331a9f212b3b3a5f79f4c01f01fe6e11c10c4d999d93` |

F1 changes coverage only when account/card/date meaning changes; description/amount corrections preserve it, save old/new values and stale-report evidence. F2 removes an untracked copied source after rollback or reports its retained path; tracked/pre-existing sources stay. F3 builds one transaction-to-support index and retains deletion preview/recheck. Tests cover preserved/invalidated periods, cleanup/unlink failure, and another observation that supports a transaction. No test, compile or lint has run after repair. Coordinator acknowledgement is required before verification. No other paths or setup changed.
