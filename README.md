# Hackathon Coding Agent Harness

A small, file-based workflow for coding agents. It uses Python's standard library and does not require Ouroboros, an MCP server, or a runtime service.

## Install in this repository

Python 3.9+ is required. To initialize this workflow in another Git repository with [`uv`](https://docs.astral.sh/uv/):

```sh
uvx --from git+https://github.com/jtrimind/hackathon harness init
```

This runs the CLI once in the current directory. To install a reusable command instead:

```sh
uv tool install git+https://github.com/jtrimind/hackathon
harness init
```

Run the command from the repository you want to initialize. `harness init` creates a blank `features.json`, a `features/` directory, `MVP.md`, requirements templates, project instructions in `AGENTS.md`, and local requirements interview, architecture planning, and feature implementation skills. It does not copy this repository's feature list or requirements.

Initialization is repeatable. Existing files are preserved and reported for review. If `AGENTS.md` already exists, the harness workflow block is appended between markers; subsequent runs update that block without adding another. Review any preserved files and merge their content with the scaffold where appropriate.

After initialization, review the requirements templates and record the project context in `MVP.md`. Add a feature only after requirements discovery. Run `harness validate` to check the scaffold. A checkout of this repository also supports `python harness.py <command>`.

## Workflow

1. Refine the product requirements with the user. Record functional and non-functional requirements with stable IDs in Markdown files under `requirements/`, summarize the MVP in `MVP.md`, and link each planned feature specification to its requirements.
2. Review the ordered feature registry and dependencies. A feature may begin only when all prerequisites are complete.
3. For one feature at a time, complete its scope, acceptance criteria, and verification commands. Obtain explicit user approval for that exact specification before changing implementation code.
4. Record approval and start the feature:

   ```sh
   harness ready <feature-id>
   harness approve <feature-id> --by-user
   harness start <feature-id>
   ```

   `--by-user` is an audit record; use it only after the user approves that exact feature specification.
5. Implement only that feature. Run its listed verification commands, record the result, and mark it complete:

   ```sh
   harness done <feature-id>
   ```

   The feature implementation skill may use a Ralph loop to fix and re-verify failures within this approved feature. The loop must not change the approved scope or specification. Stop and return to the coordinator if a specification or scope change is needed; that change requires renewed user approval and a new implementation start.

6. Report evidence and discuss the next feature separately.

The harness does not execute arbitrary verification commands. The agent runs them and reports the results.

## Commands

- `harness init` — initialize the harness in the current directory.
- `harness status` — show feature states and dependencies.
- `harness validate` — check the registry, specs, dependencies, requirement references, cycles, and ordering.
- `harness add <id> --title "..." [--depends-on id,id]` — add a feature and a specification template.
- `harness ready <id>` — check prerequisites and specification completeness.
- `harness approve <id> --by-user` — record explicit approval of the current specification revision.
- `harness start <id>` — enforce approval and prerequisite gates before implementation.
- `harness done <id>` — mark a started feature complete after verification.

## Files

- `MVP.md` — project goal, users, constraints, and sprint scope.
- `requirements/*.md` — functional and non-functional requirements with stable IDs such as `FR-001` and `NFR-001`.
- `features.json` — ordered feature registry, status, dependencies, and spec paths.
- `features/<id>.json` — feature scope, requirement IDs, acceptance criteria, verification commands, and approval record.
- `harness.py` — compatibility entry point for running the CLI from a repository checkout.
