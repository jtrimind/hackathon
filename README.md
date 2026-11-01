# Hackathon Coding Agent Harness

A small, file-based workflow for Codex and other coding agents. It does not require Ouroboros, an MCP server, a framework, or third-party Python packages.

## Start here

1. Tell the agent the product idea and constraints. Ask it to refine the requirements with you; record functional and non-functional requirements with stable IDs in Markdown files under `requirements/`, summarize the MVP in `MVP.md`, and link each planned feature specification to the requirements it addresses.
2. Review the feature order and dependency links. A feature may begin only when all its prerequisites are complete.
3. For each feature, discuss scope, acceptance criteria, and verification commands. The agent must show you the finished spec and wait for your explicit approval before touching implementation code.
4. After approval, the agent records it and starts the feature:

   ```powershell
   python harness.py ready <feature-id>
   python harness.py approve <feature-id> --by-user
   python harness.py start <feature-id>
   ```

   `--by-user` is an audit record that the user explicitly approved; it is not a substitute for asking. Do not run it unless the user has said yes to that exact feature spec.
5. Implement only that feature. Run its verification commands. Record the outcome and mark it complete:

   ```powershell
   python harness.py done <feature-id>
   ```

6. Report what changed and verification evidence. Then refine and approve the next feature separately.

## Commands

- `python harness.py status` — show feature states and dependencies.
- `python harness.py validate` — check registry, specs, dependency IDs, requirement references, cycles, and ordering.
- `python harness.py add <id> --title "..." [--depends-on id,id]` — add a feature and spec template.
- `python harness.py ready <id>` — check the spec and prerequisites before approval.
- `python harness.py approve <id> --by-user` — record explicit user approval for the current spec revision.
- `python harness.py start <id>` — enforce the approval and dependency gate before implementation.
- `python harness.py done <id>` — mark a started feature complete.

Python 3.9+ is recommended. The harness itself uses only the standard library. On macOS/Linux, replace `python` with `python3` if needed.

## Files

- `MVP.md` — user-facing MVP summary and constraints.
- `requirements/*.md` — functional and non-functional requirements with stable IDs such as `FR-001` and `NFR-001`.
- `features.json` — ordered feature registry, status, dependencies, and spec paths.
- `features/<id>.json` — feature scope, `requirement_ids`, acceptance criteria, verification commands, and approval record. Planned and in-progress features must reference at least one existing requirement ID; completed legacy features may omit links.
- `harness.py` — portable workflow gate and validation CLI.

Feature spec verification commands are run from the repository root using the current shell. Keep them focused on that feature. The harness does not run arbitrary commands automatically; the coding agent runs and reports them after implementation.
