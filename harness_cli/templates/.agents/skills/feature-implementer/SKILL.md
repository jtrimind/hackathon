---
name: feature-implementer
description: Implement and verify exactly one user-approved feature from this repository's harness when invoked as a subagent by a coordinating agent.
---

# Feature Implementer

This skill is for a subagent that has been delegated one feature ID by a coordinating agent. It does not spawn its own subagents. The coordinator owns the user conversation, requirements, feature scope, and explicit approval. Your job is to implement the approved feature exactly as specified and report the evidence.

## Before editing

1. Confirm the coordinator supplied exactly one feature ID and the intended repository/workspace. If either is missing or multiple features are requested, stop and ask the coordinator to clarify.
2. Read `AGENTS.md`, `README.md`, the feature's `features/<id>.json`, the requirements referenced by its `requirement_ids`, and any relevant `ARCHITECTURE.md` or existing project docs. Inspect the current worktree and preserve unrelated user changes.
3. Confirm the feature is `planned`. Run:

   ```powershell
   python harness.py ready <feature-id>
   python harness.py start <feature-id>
   ```

   `start` is the implementation gate: it checks prerequisites, planned status, and that the user approval matches the current feature specification. Do not call `approve` or create approval on the user's behalf. If `ready` or `start` fails, make no code changes; report the exact failure to the coordinator. If the feature is already `in_progress`, do not assume another agent's work is yours; ask the coordinator how to proceed.

## Implement the delegated feature

- Work only within the approved feature's scope and acceptance criteria. Do not implement neighboring roadmap features, alter requirement documents, or broaden the feature spec.
- Follow repository instructions and the recorded architecture. If the spec conflicts with requirements or architecture, or a necessary decision is missing, stop and ask the coordinator rather than silently changing scope.
- Keep changes focused. Inspect your diff so unrelated edits are not included.
- Run every verification command listed in the feature spec from the repository root. If a command fails, report the output and fix only issues within the approved scope. Do not mark the feature done while required verification is failing.
- You may use a Ralph loop to repeat implementation fixes and the feature's listed verification commands until they pass. Keep every iteration within the current approved scope and specification. Do not let the loop change acceptance criteria, add work from another feature, or continue into dependent features.
- Stop the loop and report to the coordinator if passing verification requires changing the specification, expanding scope, or making a decision the specification leaves open. The coordinator must get renewed user approval for the revised specification and restart the harness gate before that work proceeds.
- Treat the feature's listed verification commands as the loop's success condition. Do not run an open-ended loop across the MVP or mark the feature done unless all listed commands succeed.

After all listed verification commands succeed, record completion:

```powershell
python harness.py done <feature-id>
```

Do not continue to another feature. The coordinator will review your report and discuss the next feature with the user.

## Report to the coordinator

Return a concise report that includes:

- feature ID and final harness status;
- changed files and a short summary;
- each verification command and its result;
- any blockers, unresolved decisions, or work that could not be completed within scope.

If work cannot proceed, leave the feature in its current harness state and explain why. Never mark work done without successful verification evidence.
