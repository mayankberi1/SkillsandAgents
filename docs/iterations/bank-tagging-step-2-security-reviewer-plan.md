# BL-009 step 2 — Security Reviewer checklist

Assignment SEC-TAG-IT2 r1. Backlog revision 8; BL-009 scope 2; queue revision 8. Requirements APR-ING-REQ-006, design APR-ING-DES-005 and step approval APR-TAG-IT2-001. User accepted local storage without encryption for the initial version as APR-TAG-STORE-001. Review this accepted storage choice as scope, not as a blocker. Do not edit files, install packages, use web search or open a real history.

| Task ID | File | Planned security/privacy check | Status | Per-file verdict / evidence | Next action |
|---|---|---|---|---|---|
| SEC2-01 | `skills/bank-statement-ingestion/scripts/bank_history.py` | Input validation, authorization/scope, SQL, transactions, data minimization, no financial-field changes | Done | Fail for reviewed snapshot. Hash differed from Developer report because file changed during review. Rule evidence saved raw quote text; input fields have no size limits. The read function returns full transaction rows. | Re-review after remediation and stable hashes |
| SEC2-02 | `tests/bank_statement_ingestion/test_bank_history.py` | Generated data, unsafe input, network/dependency behavior, private-data exposure | Done | Fail. No test checks that raw chat text is excluded from stored rule evidence or that tag/source lengths and tag counts are bounded. | Add privacy/limit regression tests |
| SEC2-03 | New `skills/bank-transaction-tagging/SKILL.md` | Search-query minimization, untrusted web evidence, user consent, hallucination and disclosure risk | Done | Fail. Skill limits listed query fields but does not say descriptions and web content are untrusted instructions. It does not clearly prevent prompt-injection text from changing search behavior. | Add untrusted-text and safe-extraction rules |
| SEC2-04 | `README.md` | Accurate capability and install claims | Done | Pass. It lists the skill without unsupported privacy claims. | — |
| SEC2-05 | `skills/CATALOG.md` | Accurate dependencies and capability claims | Done | Pass. It states the helper and approved search-tool need accurately. | — |
| SEC2-06 | `tests/bank_statement_ingestion/test_distribution.py` | Test isolation, network blocking, data handling | Done | Fail. It does not assert the untrusted-text, unanswered-user, or evidence-minimization rules. | Extend distribution assertions |
| SEC2-07 | Cross-file data flow | Trace sensitive fields from saved transaction to web search and persistence; check account/currency boundaries | Done | Fail. Raw descriptions reach the agent. Skill instructions are the only boundary before web search. No direct Python web call exists. | Minimize returned fields and make safe-search rules explicit |
| SEC2-08 | Baseline and verification evidence | Compare current hashes with Developer's baseline/final evidence; state limits | Done | Fail. At review time `bank_history.py` hash was `af227489d248fa245ef5322a74a1260daf368713857ea7d9decd7698ba98ee61`, not the Developer's reported hash. Developer was editing a fix concurrently; this is an unstable snapshot, not evidence of an unexplained post-test edit. | Review only after a stable final hash is saved |

No real financial data or web request will be used.

## Review result

Fail pending remediation. High risk: transaction descriptions and web results are untrusted text, but the skill does not say to ignore instructions inside them. A malicious description may try to add private details to a search. Medium risk: rule evidence stores a raw user quote, contrary to the saved Coordinator interpretation. Medium risk: partial updates clear source evidence; this matches the Code Reviewer finding. Medium risk: tags-only choices may be overwritten; this matches the Code Reviewer finding. Lower risks: rule-applied statuses are wrong; input lengths and tag counts are not bounded. The reviewer did not run tests, scanners, web searches, or use real data.
