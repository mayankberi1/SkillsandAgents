---
name: solution-design
description: "Design implementable component, API and data contracts."
---

# solution-design

## Activation and inputs

Design implementable component, API and data contracts. Relevant roles: Solution Designer, Architect, Developer. Inputs: Approved requirements/architecture and UI constraints. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

start with first identifying the most significant decisions to be made and ask users for those decisions while suggesting recommended approaches.

Apply the shared collaborative discovery policy. Walk through concrete inputs/outputs, contracts, validation, integrations and error/recovery scenarios with the user where behaviour is unclear. Resolve material questions and favour understandable component names and straightforward interactions.

Specify responsibilities, APIs, data models, validation and error paths. Evaluate classes/interfaces/composition/inheritance only where meaningful. Assess all five SOLID principles and genuine pattern opportunities. Diagram significant classes/interactions/data transformations/storage/trust boundaries without redundant views. Verify design fits scope and existing code.

show the user the internal working of each code file at high level and the classes, objects, and types so the user can approve it.

## Outputs and boundaries

Detailed design proposal and implementation contracts. Include decisions, deliverable references, evidence, risks/blockers and next action. Architecture defines boundaries; documentation-diagrams maintains views.
