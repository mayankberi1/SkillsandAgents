# Bank statement format revision 2 — Security reviewer checklist

Assignment SEC-BANK-FMT-002 r1. Backlog BL-001, scope revision 9, implementation security review. Approval APR-ING-IT4-001. Read-only review of the six approved code, skill and test paths. Baseline and implementation hashes are listed in [the developer plan](bank-statement-format-r2-developer-plan.md).

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| SR-001 | Six approved files and current hashes | Reconcile actual paths and hashes with developer plan | Done | All six first-review hashes matched the Developer plan. | Recheck after repair. |
| SR-002 | `bank_history.py` | Review input validation, source/file checks, exact conversion, stored evidence, failure paths and statement transaction behavior | Done | **Fail.** Medium: amount marks accept letters and Unicode digits, which can alter a saved amount. Low: date patterns have no length cap before `strptime`. Source checks and whole-statement stop remain in place. | Re-review repaired code. |
| SR-003 | `SKILL.md` | Review format instructions, privacy boundaries and error handling | Done | **Fail.** It describes the same overly broad separator acceptance; update after code correction. | Re-review repaired instructions. |
| SR-004 | Four assigned test files | Review whether tests cover security and fail-closed acceptance cases | Done | Pass for reviewed paths. The new separator and long-pattern edge tests were missing at first review. | Re-review added cases. |
| SR-005 | Cross-file security | Check all six files for secrets, unsafe evaluation, path risks, data leakage and scope drift | Done | No other findings. Source/hash/permission checks and write boundary remain in place. No real data, installs or network access. | Recheck after repair. |
| SR-006 | Security result | Record per-file verdicts, findings and review limits | Done | Initial verdicts: `bank_history.py` Fail; `SKILL.md` Fail; all four test files Pass. No automated security scan was supplied. Original pre-edit copies were unavailable, so no byte-level baseline comparison. | Re-review repairs; retain this failed attempt. |

## Initial checkpoint

The reviewer read the developer plan, agent-planning and security-privacy instructions. The initial checkpoint was acknowledged. The review found the issues recorded above. The Coordinator assigned the two validation repairs within the approved scope; re-review is required. No tests, installs, network access or real history were used by the reviewer.
