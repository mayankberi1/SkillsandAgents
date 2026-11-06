# Amount-format evidence design checklist

Assignment DESIGN-BANK-FMT-002 r1. BL-001 scope revision 9, design clarification after implementation review. Related approvals: APR-ING-DES-006 and APR-ING-IT4-001. This review does not change the approved design or implementation.

| Task ID | File / criterion / deliverable | Planned action | Status | Result and evidence | Blocker / next action |
|---|---|---|---|---|---|
| AED-001 | Approved revision 5 and assignment | Reconcile scope, approvals and precise design statement about unclear separator meaning | Done | Revision 5 says unclear amount separator meaning needs source evidence or a user answer. | — |
| AED-002 | Current Record and amount conversion | Inspect inputs, evidence checks and save flow | Done | `Record` has amount format strings, text and location, but no format evidence field or check. Current conversion accepts a supplied interpretation without proving it. | — |
| AED-003 | Amount format ambiguity | Propose exact caller input, ambiguity rule, source/user evidence handling and error behavior | Done | Proposed `amount_format_evidence: Evidence | None`, check matching user answer or source evidence, and raise whole-file `FormatError` when evidence is missing/conflicting. Classified as clarification within approved intent. | User approval requested. |
| AED-004 | Excel serial date epoch | Assess whether the supplied epoch and current evidence check prevent wrong-basis conversion; propose a safe minimal rule and tests | Done | Reader knows epoch but does not expose it; history accepts missing `canonical_date`. Proposed expose 1900/1904 epoch and require match; styled dates also require matching canonical date. Wrong or missing basis becomes whole-file `FormatError`. This adds `statement_reader.py`, which the approved step excludes. | User approval requested for scope expansion. |
| AED-005 | Tests and approval status | Define test cases and classify clarification vs material scope change | Done | Amount cases: missing, matching/conflicting user evidence, valid/invalid source evidence, clear format without evidence, no-save. Epoch cases: both matching bases, mismatch/no-save, styled date without canonical date, nonnumeric serial, reader invalid/missing epoch, non-date patterns unchanged. | Await user decisions. |

## Initial checkpoint

The Solution Designer read the solution-design and agent-planning instructions. The Coordinator acknowledged the checklist before review. The evidence proposals above are complete. No code or design files were changed by the Solution Designer. User decisions are pending for the proposed evidence contract and reader scope change.
