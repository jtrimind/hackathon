# Functional Requirements

### FR-001: Feature-to-requirement traceability
- **Statement:** Each new or active feature specification identifies one or more functional or non-functional requirement IDs that it addresses.
- **Actor/context:** The person planning a feature and the hackathon harness.
- **Conditions and exceptions:** Existing completed feature specifications may lack links; new or in-progress work requires them.
- **Acceptance or verification:** Feature specifications contain requirement IDs that the harness can check against the requirements documents.
- **Status:** Confirmed
- **Source:** User request to connect features to requirements.

### FR-002: Validate requirement references
- **Statement:** The harness validates that active feature specifications include requirement IDs and that every referenced ID exists in the project's functional or non-functional requirements documents.
- **Actor/context:** The `validate`, `ready`, and `approve` workflow before implementation begins.
- **Conditions and exceptions:** Completed legacy feature specifications without requirement links remain valid; if they contain links, those links must resolve.
- **Acceptance or verification:** Missing or unknown IDs are reported with the affected feature and identifier before implementation can start.
- **Status:** Assumption
- **Source:** Proposed implementation of the user's traceability request; pending approval of this feature specification.

### FR-003: Implement an approved feature in a subagent
- **Statement:** A separate implementation skill can be invoked in a subagent with one approved feature ID, implement and verify only that feature, and report the outcome.
- **Actor/context:** A coordinating agent delegates an approved feature from this repository's harness to a subagent.
- **Conditions and exceptions:** The subagent must honor the current feature specification, prerequisite status, explicit user approval, and repository instructions; it stops and reports if any gate is not satisfied.
- **Acceptance or verification:** The skill starts through the harness gate, runs the feature's listed verification commands, marks the feature done only after successful verification, and returns a concise evidence-based report.
- **Status:** Confirmed
- **Source:** User request for a separate implementation skill to run in a subagent.

### FR-004: Initialize the harness in another repository
- **Statement:** A user can set up the file-based harness and its project-local skills in another repository using one or two simple commands.
- **Actor/context:** A developer starting to use the harness in an existing or new project.
- **Conditions and exceptions:** Existing project files must be preserved; initialization should create missing scaffold files and clearly report conflicts.
- **Acceptance or verification:** A command initializes the local feature registry, requirements templates, instructions, and skills so the repository can use the existing feature workflow.
- **Status:** Confirmed
- **Source:** User request to make this harness easy to set up in other repositories, informed by the Q00/ouroboros installation flow.

### FR-005: Provide a reusable guide for the preferred project stack
- **Statement:** The harness provides a project-local skill and supporting reference files that help users start projects using the default preferred stack: TypeScript, Next.js, NestJS, PostgreSQL, Prisma ORM, and pnpm.
- **Actor/context:** A user planning a new project with this harness and the architecture-planning skill.
- **Conditions and exceptions:** The stack remains a preference. The guide explains when a technology may not apply or another choice may fit better. Project planning must verify current details that could have changed.
- **Acceptance or verification:** The guide covers each technology's role and fit, relevant interoperability and compatibility, a practical starter architecture and implementation sequence, key pitfalls, and official source links with a checked date; the architecture-planning skill directs agents to consult it and recheck time-sensitive details.
- **Status:** Confirmed
- **Source:** User request to prepare reusable information files for the common preferred stack; user selected a practical guide including compatibility and starter structure.
