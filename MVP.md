# MVP

## Summary

A project-local Codex skill guides agents through a consistent requirements interview before they plan implementation work in this hackathon repository.

## Users and problem

- Users: People using Codex to refine a hackathon product idea in this repository.
- Problem: The current workflow does not prescribe which requirements questions the agent must ask, so important context may be missed between projects or sessions.

## In scope

- A discoverable project-local skill with a required question set and an interview procedure.
- Produce separate, traceable functional and non-functional requirements files from the completed interview using reusable templates.
- Before proposing first-version scope, explicitly review common capability candidates across identity/access, data management, discovery, workflow, communication, administration, integrations, and operational quality; select relevant examples and record whether each is needed, not needed, deferred, or unresolved.
- Keep the full feature map as a roadmap, but recommend one small, independently verifiable next feature for implementation at a time; discuss the next feature only after the current one is complete.
- Link each planned feature specification to the functional or non-functional requirements it addresses, and validate that the referenced requirement IDs exist before approval or start.
- Provide a separate subagent-oriented implementation skill that consumes one approved feature specification, implements and verifies only that feature, and reports the result.
- Provide a downstream project-local architecture planning skill that uses reviewed requirements and the feature roadmap to recommend an architecture and technology stack, then records user-confirmed decisions.
- Prefer languages and frameworks that make implementation errors easy for AI-assisted review to detect and explain through strong typing, static analysis, clear diagnostics, and automated checks; require the architecture record to name concrete stack choices with rationale.
- For each meaningful answer, consider relevant exceptions, edge cases, and outlier situations; ask focused follow-up questions when they could change the requirements.
- Identify stakeholders relevant to the idea, including users split into meaningful roles such as operator and end user.
- For each relevant stakeholder group or user role, discuss what they want to achieve and what currently makes it difficult; capture conflicting goals when they emerge, without requiring a primary stakeholder ranking.
- Explore the relevant situation (when and where the problem occurs, and how it is handled today) and desired outcomes before discussing possible product outputs; ask about environment or tools when relevant. Once enough context is gathered, suggest a few suitable output forms with tradeoffs and decide with the user rather than assuming one up front.
- Ask openly about any constraints that could shape the solution, using examples such as legal or regulatory requirements, privacy, technology, schedule, budget, or organizational context only as prompts; clarify which are firm requirements and which are preferences.
- First synthesize the initial project information and interview answers into a requirements brief, distinguishing confirmed decisions from assumptions and unresolved questions; show it to the user for review before deciding first-version feature scope.
- After requirements review, organize relevant feature candidates. Mark independent and cross-cutting capabilities, and show prerequisite relationships among dependent features.
- Use that feature map to propose first-version scope options and a minimal, coherent MVP recommendation, including necessary prerequisites; discuss exclusions, success criteria, and verification with the user.
- Identify which agreed features belong to the current sprint; list that scope and the next-review candidates outside the sprint separately in `MVP.md`, and track current sprint implementation states in the existing registry.
- Capture requirements and the agreed MVP in `MVP.md`; keep the ordered feature registry and individual specifications in `features.json` and `features/`.

## Out of scope

- Requiring the `harness.py` CLI to conduct the requirements interview itself.
- A general-purpose interview skill for unrelated repositories.

## Constraints

- Keep the skill local to this repository under `.agents/skills/`.
- Keep hackathon feature approval gates in force; interview or plan approval is not implementation approval.
- Keep features small and independently verifiable.
