---
name: user-profile
description: >
  Store, read, update, and manage comprehensive user profiles including demographics, location,
  preferences, interests, and projects. Use when a user asks to remember information about themselves,
  update their profile, or when an agent needs contextual personal data for personalised responses.
  Trigger on: "save my profile", "what do you know about me", "update my info", "remember this",
  "user data", "preferences", "interests", "projects I'm working on".
---

# User Profile Skill

## When to Use
- User explicitly asks to save, update, or query their profile.
- Agent notices relevant personal information in conversation (implicit capture) that matches a defined profile category.
- A new user interaction begins where no profile exists yet (triggers onboarding).

## 1. Trigger Recognition
### 1.1 Explicit Triggers
Recognize these direct commands from the user:
- **Save/Store**: "remember this", "save my info"
- **Update**: "change my job title to X", "update my preferences"
- **Query**: "what do you know about me?", "show my profile"
- **Delete**: "delete my age", "clear my profile"
- **Onboarding**: user starts a new session with no prior profile

**Priority Order:** If multiple triggers match in one message, prioritize: Delete > Save/Update > Query > Onboarding.

### 1.2 Implicit Triggers
Detect profile-relevant information shared casually in conversation:
- High Confidence (act after brief confirmation): Direct statements like "I'm a senior engineer at Stripe" or "Based in London".
- Medium Confidence (note for later context): Strong implications like "Just finished deploying my Go microservice". Do not persist to the file without explicit user agreement.
- Low Confidence (skip vague hints): e.g., "I like building stuff".

## 2. Storage Mechanics
### 2.1 Format: Markdown (.md)
The profile is stored as a strictly formatted Markdown file using `##` sections and `- Key: Value` list items.

**Storage Paths:**
- **Project-scoped** (Active in project context): `.user-profile.md` in the current project root.
- **Global-scoped** (Fallback or standalone): `~/.config/user-profile/USER-PROFILE.md`.

If both a project-scoped profile (`.user-profile.md`) and a global profile (`~/.config/user-profile/USER-PROFILE.md`) exist, always read from the project-scoped path first (it shadows the global during active sessions). Display a brief notice on first read in that context: *"A local profile was found for this project alongside your global profile — showing project data only."* During writes to the project path, never modify or touch the global file.

### 2.2 Profile Schema (Markdown Structure)
Always maintain this exact section order and formatting:

```markdown
# User Profile

## Metadata
- created_at: [ISO 8601 timestamp]
- last_updated: [ISO 8601 timestamp]
- source: batch | explicit | implicit
- version: [integer]

## Identity
- name: [Full or preferred name]
- pronouns: [he/him, she/her, they/them, etc.]
- avatar_url: [Optional URL]

## Demographics
- age: [Numeric or range]
- city: [City name]
- country: [Country name]
- timezone: [e.g., Europe/Berlin, UTC+5:30]
- language: [e.g., en, es, hi]

## Professional
- title: [Job title]
- company: [Employer name]
- industry: [Industry keyword]
- skills: [Comma-separated list, e.g., Python, Go, React]
- experience_level: entry | mid | senior | lead | principal

## Preferences
- communication_style: concise | detailed | casual | formal
- verbosity: brief | moderate | thorough
- units_of_measurement: metric | imperial

## Interests
- [Interest 1]
- [Interest 2]

## Goals
- [Goal 1]
- [Goal 2]

## Projects
### Project 1: [Project Name]
- status: active | paused | completed | archived
- role: [User's role]
- tech_stack: [Comma-separated list of tools/technologies]
```
*(Note: For each new project, increment the `### Project N:` header by 1).*

## 3. Profile Operations

### 3.1 First Use — Batch Collection
When the skill detects no profile exists (or the file only contains scaffolding/defaults):
1. Inform user: *"I don't have a profile for you yet. Want to set one up? I'll ask one question per category."*
2. **Obtain Consent**: Explicitly confirm they are okay with storing this data locally before proceeding.
3. **One Question Per Category** (max 6 messages total). Present the category and ask for the value. If skipped, leave it empty or use safe defaults.
4. After all questions are answered or skipped, write the complete profile to the target path using the template in `assets/profile-template.md`.

### 3.2 Reading a Profile
1. Check project scope (`.user-profile.md`) first; fall back to global if missing.
2. Display data in a clean, readable summary. Never dump raw Markdown text unless asked.
3. Report profile completeness (e.g., *"Your profile is 60% complete."*).

### 3.3 Incremental Updates (Merge Rules)
When updating fields, strictly follow these rules to avoid losing sibling data:
- **Scalar Values (Single Line)** — Perform a targeted line replacement using this procedure:
  1. Locate the exact line matching `- <key>: ` (the key must be a full match, not a prefix — e.g., `- name:` matches only `name`, not `nickname`).
  2. Split the line at the **first** colon followed by a space (`: `). Everything before that is the key; everything after is the current value.
  3. Replace only the portion after `: ` with the new value. Preserve all leading whitespace, dashes, and indentation.
  4. If the new value itself contains a colon (e.g., `- avatar_url: https://example.com/photo.jpg`), split at the **first** occurrence of `: ` only — everything after it is the value, including subsequent colons.

  *Example*: Updating `title` in Professional from "Software Engineer" to "Senior Software Engineer":
  - Find line: `- title: Software Engineer`
  - Split at first `: ` → key=`title`, old value=`Software Engineer`
  - Replace: `- title: Senior Software Engineer` (all other keys under `## Professional` are untouched)
- **Arrays (Comma-separated Lines)**: For lines like `- skills: Python, Go`, append new items as a comma-separated list if they aren't already present.
- **Projects**: To add a project, scan existing `### Project N:` headers, determine the highest `N`, and append a new block with `N+1`.

### 3.4 Implicit Capture Confirmation
When catching high-confidence info from conversation:
1. Confirm before writing: *"I noticed you mentioned [X]. Is it okay if I save that to your profile?"*
2. If the value conflicts with existing data, prompt: *"Your profile says [Current], but you mentioned [New]. Update it?"*

### 3.5 Correction Flow
If a user corrects an implicit capture (*"I never said that"*):
1. Remove the specific entry or line from the file immediately.
2. Ask: *"Should I remove just this entry, or pause all implicit capture for this session?"*

### 3.6 Context-Aware Gap Detection
During relevant conversations, prompt for missing data once per session:
- *Example*: If discussing coding tasks and `skills` is empty, ask about their tech stack. If scheduling a task and `timezone` is empty, ask for their timezone.

### 3.7 Deleting Profile Data
- Confirm exactly what will be removed before editing.
- For soft-deletes, move the target section or clear the values but keep the file structure intact.

### Hard Delete (Permanent Destruction)
When a user explicitly requests permanent profile destruction:
1. **Confirm Intent:** *"Permanently delete your entire profile? This cannot be undone."*
2. **Delete File(s):** Remove the project-scoped `.user-profile.md` and/or global `~/.config/user-profile/USER-PROFILE.md`.
3. **Verify Deletion:** Attempt to read the path. If it no longer exists, deletion is successful. Report failure to the user if permissions or errors persist.

## 4. Metadata Enrichment
Every write operation must update the `## Metadata` block at the very top of the file:
- `created_at`: Set once on first creation; never change afterwards.
- `last_updated`: Update to current ISO timestamp on every single write.
- `source`: Reflect the write method (`batch`, `explicit`, or `implicit`).
- `version`: Integer that increments by 1 on every non-batch write (explicit, implicit, or correction). Preserved as-is during initial batch creation.

## 5. Privacy & Ethics
- **Transparency**: Always inform users when data was inferred from chat vs explicitly stated.
- **Data Minimization**: Default to the least precise useful representation (e.g., country-level instead of street address). Do not store highly sensitive info unless explicitly necessary for a task.
- **Review**: Periodically offer to review and clean up stale or outdated profile entries.
