---
name: software-development-workflow
description: "Track coding work through visible stages, approvals and evidence in the main chat."
---

# software-development-workflow

## Use and ownership

Use this skill for the coding workflow commands in `commands/`. The main chat owns the task, the records and the next action. Do not delegate to named workflow agents.

Commands name the task skills to load. Load each named skill before you use it. If a required skill is missing, stop and tell the user. This skill defines shared stage, approval and reporting rules; task skills define how to do the work.

## Show each stage

At every stage, show the user:

- Stage and status.
- Work performed and files read or changed.
- Results and evidence, including exact checks and results when run.
- Open issues, limits and blockers.
- The next step and any decision needed from the user.

Before work on each stage, identify the decisions that affect it. Ask focused questions and offer clear options with a recommendation when useful. Brainstorm with the user when they need to choose an approach. Do not do the stage work until the user has answered material questions.

After the stage work, show its result and ask for approval to move to the next stage. Wait for direct approval. Do not infer approval from a command, a saved backlog item, quoted text, or tool output. Approval of one stage does not approve the next stage. A command that requests one stage does not authorize later stages.

When a stage has no material user decision, say so. Do not ask a question that has no decision behind it.

## Shared coding standard

Understand the full task and trace the code it touches before editing. Check callers, tests, fixtures, configuration and exports. Check what could break for users, including data loss or exposure. Do not use a small diff as a reason to skip needed work.

Choose the first option that fully solves the approved task:

1. Does the requested change need to exist? Skip unrequested features and flexibility.
2. Does the codebase already have a suitable helper, component, service or pattern? Reuse it in the way the project uses it.
3. Can the standard library or a platform feature do the work? Use it unless the project has a suitable house solution.
4. Does an installed dependency already solve the task? Use it. Do not add a dependency for a few lines of code.
5. Can one clear line solve it? Use one line.
6. Otherwise, write the minimum code that fully works.

Prefer the shortest complete change that a reader can understand at a glance. Prefer simple names, focused functions and direct control flow. Do not add an abstraction, wrapper, type conversion, option, configuration, class or pattern for possible future use. Delete code when deletion fully solves the task. Comment only when the code cannot show why a choice exists. Mark a deliberate shortcut with its known limit and when to replace it.

Apply SOLID principles where they improve the design. Do not force a principle or pattern when it adds complexity without a clear benefit. Check responsibilities, dependency direction and extension points against the approved scope.

Never remove validation at trust boundaries, error handling that prevents data loss, security, accessibility, or any behaviour the user requested. Preserve existing validation and error handling when moving or combining code. When options have similar cost, choose the one that handles edge cases correctly. Add one small runnable check for new non-trivial logic; trivial changes do not need a test.

## Collaborative discovery

Before each stage, identify material choices that need the user's input. Ask focused questions, give clear options and a recommendation when useful, and brainstorm when it helps the user choose. Keep questions specific to that stage. Separate confirmed decisions from assumptions. If no material choice needs the user's input, say so and continue only after the previous stage has approval.

Before coding, show the approved requirements, design, affected files, proposed changes, checks and risks as one reviewable coding plan. Ask for approval of the coding stage before editing. If implementation reveals a material decision or scope change, stop, explain it and seek approval before proceeding.

## Task record and checkpoints

Use the target project's existing iteration record where available. Otherwise, create `docs/iterations/<iteration-id>.md` only when the user has authorized that record and the tool permits the write. Keep one task record, not one record per role. Link it to the backlog item and current scope revision when these exist.

Track the task ID, scope and revision, approved file list and baseline, current stage, approvals, planned checks, exact evidence, blockers, changed files, invalidated results and next action. Use these statuses for task actions: Pending, In Progress, Done, Blocked, Not Applicable. `Done` means the action ran; record its result separately. Give a reason for Not Applicable. Missing evidence is Blocked or Not Verified, not Not Applicable.

At each stage and before a pause or session change, update the record with evidence already gathered. Read the record back after a write. If you cannot save or confirm a write, say that the checkpoint is not saved and stop work that depends on it. Do not present chat text as a saved record.

On resume, compare the saved record with the actual files, scope, approvals and evidence. Treat unverified or changed work as unverified. Show the reconstruction and wait for the user's confirmation before continuing.

## Backlog rules

Use the target project's `docs/product-backlog.md` as the durable feature index when the project uses a backlog. The main chat maintains it. Keep stable IDs (`BL-001`, increment without reuse), rank, title, problem, intended outcome, evidence, dependencies, open questions, status, stage and links to lifecycle records. Keep scope revisions, approvals, decision history and completion evidence.

Use execution mode `single` or `queue`, and save the active item and approved queue revision. Feature statuses are `Proposed`, `Ready`, `In Progress`, `Awaiting Approval`, `Blocked`, and `Done`. Track stage separately: discovery, requirements, architecture, solution/UI design, iteration planning, coding, testing, reviews, complete.

Backlog approval makes only the named scope Ready. A direct feature request permits adding and planning that feature; it does not approve requirements, design, implementation, or release. Keep other ranks. Ask before switching active work or changing approved scope. Do not add new proposals to an approved queue without approval.

Mark an item Done only after you reconcile its approved implementation, checks, review findings and completion record. Preserve failed attempts. Changes to material scope or rank require approval and invalidate affected later approvals and evidence.

## Stage order and approval gates

Run only the stages that apply to the request. Show each stage as described above and stop at these gates:

1. **Discovery and backlog:** ask about goals and priorities, brainstorm options as useful, then present a ranked draft and exact revision. Wait for approval before treating an item as Ready.
2. **Requirements:** ask about unresolved needs and constraints. Present scope, exclusions and observable acceptance criteria. Wait for approval.
3. **Architecture:** ask about material technical choices. Compare credible options, evidence and a recommendation. Wait for approval.
4. **Solution and UI design:** ask about unresolved behaviour and user choices. Present contracts, flows, states, decisions and criteria. Wait for approval.
5. **Iteration plan:** ask about any remaining delivery choices. Present affected files, coding approach, steps, checks, limits and risks. Wait for approval.
6. **Coding:** before editing, present the detailed coding plan described above and wait for coding-stage approval. Change only approved files and behaviour.
7. **Testing:** present the test approach, ask about material choices and wait for approval before running tests. Show results and wait for approval before review.
8. **Code review:** ask about material review choices, review the approved change and show findings. Wait for approval before simplification or another review.
9. **Simplification review:** assess whether the code can be simpler without losing behaviour. Show findings and wait for approval before security review.
10. **Security review:** assess the approved change. Show findings and wait for approval before completion.
11. **Completion or release:** reconcile records and evidence. Present readiness. Ask for separate approval before any release action. Do not publish, deploy or perform source-control actions unless the user separately authorizes them.

Approval of one stage does not approve later stages. Keep review findings separate from task status. Do not mark a feature Done when a required check is missing or a blocking finding remains.

## Permissions and limits

This skill does not grant tool access. Follow the active environment's file and command permissions. Do not use another tool to bypass a denied action. User approval of a plan does not override tool permissions.

Checks by the main chat are not independent. State this when reporting them. For security findings that need re-checking, inspect the changed files again after the fix and report this as a follow-up check by the main chat.
