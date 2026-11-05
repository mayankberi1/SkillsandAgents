---
name: software-development-design
description: "Design implementable component, API and data contracts."
---

# software-development-design

## Activation and inputs

Design implementable component, API and data contracts. Inputs: Approved requirements, architecture and UI constraints. Read applicable central AGENTS.md; this capability grants no additional authorisation.

## Procedure

Before design work, identify material decisions and ask the user focused questions. Offer options and recommendations. Brainstorm contracts, validation, integrations and error/recovery scenarios with the user where behaviour is unclear. Resolve material questions and favour understandable component names and straightforward interactions.

Specify responsibilities, APIs, data models, validation and error paths. Evaluate classes/interfaces/composition/inheritance only where meaningful. Assess all five SOLID principles and genuine pattern opportunities. Diagram significant classes/interactions/data transformations/storage/trust boundaries without redundant views. Verify design fits scope and existing code.

List every affected or new file and its purpose. For each file, list the new or changed functions, classes, interfaces, types, and other key code structures, and state the purpose of each. Mark existing structures separately from new ones. If implementation details remain uncertain, state that clearly instead of inventing names. Include the main inputs, outputs, responsibilities and links between the structures. Present this file and code structure list, contracts, flows, states and decisions as part of the complete design. Wait for design approval before iteration planning or coding starts.

## Outputs and boundaries

Detailed design proposal and implementation contracts. Include decisions, deliverable references, evidence, risks/blockers and next action. Architecture defines boundaries; software-development-documentation maintains views.
