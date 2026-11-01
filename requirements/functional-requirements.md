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
