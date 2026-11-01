<!-- hackathon-harness:start -->
## Hackathon harness workflow

Use the file-based workflow documented in `README.md` (install or initialize the harness if that file is not present).

- Keep the MVP summary in `MVP.md`, the ordered feature registry in `features.json`, and one specification per feature in `features/`.
- Clarify and record requirements and MVP scope before implementation. Split work into small, independently verifiable features, record dependencies, and put prerequisites first.
- Before editing implementation code, complete the feature spec (scope, acceptance criteria, verification commands), then obtain explicit user approval for that exact revision.
- Run `harness ready <id>`, record user approval with `harness approve <id> --by-user`, and then run `harness start <id>`.
- Implement one feature at a time. Run its listed verification commands, then use `harness done <id>` and report evidence before discussing the next feature.
- If a spec changes after approval, approval is invalidated. Do not start dependent features until prerequisites are complete.
<!-- hackathon-harness:end -->
