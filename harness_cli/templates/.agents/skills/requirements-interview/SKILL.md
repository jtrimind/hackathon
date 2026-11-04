---
name: requirements-interview
description: Guide a conversational requirements interview for product ideas in this hackathon repository, then organize the requirements, feature map, and sprint scope before implementation planning.
---

# Requirements Interview

Use this skill when someone brings a product idea or asks to refine requirements for this repository. First read `README.md`, `AGENTS.md`, `MVP.md`, `features.json`, and any project materials relevant to the idea. Follow more specific repository instructions where they apply.

## Interview approach

- Treat this as a conversation, not a form. Ask one main question at a time, or a few tightly related questions when that makes answering easier. Use answers to shape follow-ups; do not dump the whole question set at once.
- When practical, pair an interview question with a short set of relevant answer options and an explicit way to answer freely (for example, “Something else / tell me in your own words”). Keep options illustrative rather than exhaustive, include “not sure yet” when useful, and avoid forcing a choice when the topic is genuinely open-ended or options would bias the answer.
- Start from what the user has already provided. Summarize known information, separate confirmed facts from assumptions, and ask only about important gaps or ambiguities.
- Keep a running, concise summary of decisions and open questions. Do not silently turn an assumption into a confirmed requirement.
- Help the user reason through the product and its possible outcomes. Offer examples when useful, without treating examples as exhaustive choices or making decisions for the user.
- Keep requirements discovery and first-version feature selection in separate stages. Finish and share a requirements brief for user review first. Incorporate corrections before discussing which features belong in the hackathon's first version.
- For each meaningful answer, consider whether a relevant exception, boundary, or outlier could change the requirement. Ask a focused follow-up when it could; do not ask about every imaginable edge case.

## Exception and outlier check

Pay particular attention to absolute or broad statements such as "all," "always," "never," and "must." Check who or what the rule covers, when it applies, and when it might not apply. For example, "all employees must be assigned" may depend on whether an employee is scheduled and available to work that day.

Generate a few context-relevant possibilities using lenses such as:

- actor or entity states, including inactive, absent, on leave, or newly added;
- availability, eligibility, permissions, or qualifications;
- timing and changes in state;
- conflicts or limited resources;
- missing, invalid, or contradictory information;
- failure, cancellation, and recovery.

These are prompts for reasoning, not a checklist to read to the user. Ask a concise follow-up only when different answers would materially change scope, behavior, workflow, or acceptance criteria. Tailor it to the user's domain and make clear when a scenario is hypothetical. Do not decide the policy yourself. Record what the user confirms, and leave uncertain exceptions as assumptions or open questions.

## Topics to cover

Cover these topics over the course of the interview. Adapt their order and depth to the idea, and skip a follow-up when the existing information already answers it.

1. **Relevant stakeholders and user roles.** Find the people or groups actually related to the idea. Consider direct users in distinct roles, such as operators and end users, as well as decision-makers, payers, support staff, or affected groups when relevant. Do not force irrelevant categories or rank stakeholders. For each relevant group or role, explore what they want to achieve and what currently makes that difficult. Capture differences or conflicts among goals when they emerge.
2. **Shared terminology and domain concepts.** After identifying relevant stakeholders, check whether they use different words for the same concept or the same word with different meanings. Ask focused questions about terms that affect goals, process, data, decisions, or acceptance criteria. For example: “When you say ‘complete,’ what has happened?”, “Do other groups call this something else?”, or “Does this term mean the same thing to everyone?” Record stakeholder-specific wording, meanings, any agreed definition, and unresolved differences in a concise glossary when the distinctions matter. Treat this as lightweight vocabulary alignment; introduce a formal ontology or concept model only if the domain's complexity or relationships make it useful. Do not force a glossary for ordinary terms or silently choose one stakeholder's definition.
3. **Situation and current process.** Learn when and where the problem occurs and how it is handled today. Ask about the environment or tools when relevant. Use the agreed vocabulary where available, and follow up when a term reveals different process steps or states.
4. **Constraints.** Ask openly whether anything could shape or limit a solution. Legal or regulatory requirements, privacy, technology, timing, budget, resources, and organizational context can be prompts, not a closed checklist. Clarify whether a stated constraint is a firm requirement or a preference. Record the user's understanding faithfully and leave uncertain applicability as an open question.
5. **Desired outcome and possible deliverables.** First understand the stakeholder goals, problem, situation, and constraints. Then suggest a few output forms that fit the gathered information and discuss their tradeoffs with the user. Do not assume an app, website, document, or other deliverable before that discussion.
6. **Review the requirements brief.** Before selecting MVP features, synthesize the initial project information and interview answers into separate functional and non-functional requirements files. Share both files with the user, including confirmed requirements, assumptions, and unresolved questions, and incorporate their corrections. Include a concise glossary or unresolved terminology questions when they affect requirements. Do not ask them to choose a vague product direction as a proxy for first-version scope during requirements discovery.
7. **Review common service capabilities.** After the requirements brief is reviewed and before finalizing the feature map, check which common capabilities are relevant. Use the catalog below to prompt reasoning, not as a mandatory checklist. For each relevant candidate, establish whether it belongs in the first version, is not needed (with a brief reason), is deferred, or remains unresolved.
8. **Feature map after requirements and capability review.** Map the required and deferred capabilities. Organize them into independent features, cross-cutting capabilities, and features with prerequisites; record dependency order. Make dependencies understandable and include prerequisites in any proposed scope that needs them.
9. **Recommend the next feature.** Keep the complete feature map as a roadmap, but break broad end-to-end flows into small, independently verifiable features. Recommend one next feature, explain the user value and prerequisites, and ask whether to take that feature forward first. Do not ask the user to choose between large A/B bundles or commit to every feature in the roadmap at once. Do not ask a separate question just to sketch a user flow. Mention remaining capabilities as later candidates, not as current implementation commitments.

## Common capability review

Offer only examples that fit the product context; do not read the entire catalog to the user. The categories are starting points and may be extended when the idea suggests another shared capability:

- **Identity and access:** login or anonymous use, authentication, roles and permissions, account creation/recovery/deactivation, separation of user data.
- **Data management:** create, view, edit, delete, bulk actions, import/export, history or audit trail.
- **Finding information:** search, filtering, sorting, saved views.
- **Workflows and collaboration:** assignment, approvals, status changes, comments, handoffs.
- **Communication:** notifications, delivery channels, notification preferences.
- **Administration:** user management, configuration, operational controls.
- **Reporting:** dashboards, exports, analytics, activity summaries.
- **Integrations:** external systems, APIs, identity providers, scheduled data exchange.
- **Operational and quality needs:** security, privacy, accessibility, localization, reliability, backup, recovery, monitoring.

For a user-facing service, explicitly resolve identity/login and access control as needed for the first version, not needed, deferred, or unresolved. If a requirement says users see their own data, private records, or role-specific screens/actions, ask how the service will identify the user and what should be restricted. Consider the required identity or access capability as a prerequisite for those features. Do not infer that login is required simply because personal data exists, and do not infer that it is unnecessary because login was not mentioned.

Record needed capabilities as functional or non-functional requirements as appropriate. Record not-needed or deferred decisions and their rationale in the requirements summary. Keep unresolved decisions visible as open requirements. Reflect required and deferred capabilities in the feature map and dependency order before presenting first-version scope options.

## Record the result

Use the templates in `assets/functional-requirements.md` and `assets/non-functional-requirements.md` to start the requirements files. Copy and adapt them to the target project. If the target already has a requirements documentation convention, follow it instead. Never overwrite existing user-authored documents without preserving their content.

Give every requirement a stable ID (`FR-001`, `NFR-001`, and so on). Mark each item as `Confirmed`, `Assumption`, or `Open`, and include its source when practical. For functional requirements, capture expected behavior, relevant actor or context, applicable conditions and exceptions, and acceptance or verification notes when known. For non-functional requirements, record only relevant quality or constraint expectations and measurable targets when the interview supports them. Do not invent thresholds or force irrelevant quality categories. If an area has no confirmed requirement, say that it remains unspecified instead of inventing one.

When terminology differences materially affect requirements, include a short glossary in the requirements brief or link a separate glossary file. For each relevant concept, preserve the terms used by each stakeholder group and distinguish agreed definitions from assumptions or unresolved disagreements. Do not force an ontology or formal domain model when a small glossary is enough.

Update the repository artifacts in two stages:

- **Requirements review stage:** Create or update `requirements/functional-requirements.md` and `requirements/non-functional-requirements.md` with the interview findings. Distinguish confirmed content, assumptions, and unresolved questions, and preserve relevant sources. Summarize the interview in `MVP.md` and link to both files. Show the files to the user and incorporate their corrections before reviewing common capabilities. Do not finalize first-version scope in this stage.
- **Capability review stage:** Record common capability dispositions and reasons in the requirements summary. Add needed capabilities as requirements; keep unresolved ones open. Confirm identity and access decisions when the product has user-specific or role-specific access.
- **Incremental feature planning stage:** After requirements and common capability review, add the complete feature roadmap and dependencies. Split features so each can be independently specified and verified. Record one recommended next feature and its rationale; keep other capabilities as later candidates until the current feature is complete. Do not present large bundles as first-version choices.
- In `features.json`, maintain the ordered feature registry, dependencies, and existing statuses. Keep prerequisite features before dependent features. Use `planned` and `in_progress` for current-sprint features that are not yet implemented, and `done` only after the repository workflow's verification and completion step. Identify current-sprint membership and later-sprint candidates in `MVP.md` so that a planned feature outside this sprint is not reported as a current-sprint omission.
- Maintain one complete specification per feature in `features/`, including scope, acceptance criteria, and verification commands. Keep features small enough to verify independently.
- Once the user agrees to consider one feature, finish and show only that feature's specification. Do not treat agreement on the roadmap or next-feature recommendation as implementation approval.
- Summarize current-sprint features as implemented (`done`) or not yet implemented (`planned` or `in_progress`); list later candidates separately. After the selected feature is implemented and verified, report the result and discuss the next candidate before continuing.

## Approval and implementation boundary

An interview summary, deliverable discussion, feature map, or MVP proposal is not approval to implement. For each feature, complete its specification and show it to the user. Wait for explicit approval of that exact specification, then follow `AGENTS.md` and `README.md`: run `python harness.py ready <id>`, record approval with `python harness.py approve <id> --by-user`, and start only that feature. If the specification changes, obtain approval again. Work on one feature at a time, run its listed verification, record the result, and mark it done before moving to a dependent feature.
