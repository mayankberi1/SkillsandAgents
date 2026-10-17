---
name: release-readiness
description: "Assess release readiness, versions and changelog without source-control operations."
---

# release-readiness

## Activation and inputs

Prepare a release-readiness report when requested. Relevant roles: Coordinator, Developer, Code Reviewer. Inputs: Approved scope, changed-file inventory, test/review evidence and version policy. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Reconcile acceptance criteria, actual file changes, independent reviews, documentation and known exceptions. Assess compatibility and breaking-contract impacts. Propose SemVer and changelog content with evidence and blockers. Mark readiness only for verified scope; unavailable mandatory checks prevent an unqualified ready verdict.

## Outputs and boundaries

Release-readiness report, version/changelog proposal, evidence, limitations and next user decision. Do not run or delegate Git/source-control operations, generate branch/commit/merge/tag instructions, or publish a release. The user manages source control and publication manually; this skill prepares documentation only.
