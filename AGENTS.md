# Repository instructions

## Hackathon harness workflow

This repository uses the file-based, agent-neutral workflow in `README.md`. Read it before changing product code.

- Keep the MVP summary in `MVP.md`, the ordered feature registry in `features.json`, and one specification per feature in `features/`.
- Clarify the MVP with the user and record it before implementation. Split work into small, independently verifiable features. Record dependencies and put prerequisites first.
- Work on one feature at a time. Before editing implementation code, complete its spec (scope, acceptance criteria, verification commands) and obtain explicit user approval. An approval only applies to that feature and its current spec revision.
- Use `python harness.py ready <id>` to check prerequisites and spec completeness. Then obtain the user's explicit approval and record it with `python harness.py approve <id> --by-user` before `python harness.py start <id>`. Never treat approval of a plan as approval to implement.
- Run the feature's listed verification commands, record results, then use `python harness.py done <id>`.
- If the spec changes after approval, the harness invalidates approval and requires approval again. Do not start dependent features until prerequisites are complete.
- Do not run a long loop across the entire MVP. Stop after each feature, report evidence, and discuss the next feature with the user.
