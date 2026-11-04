---
name: architecture-planning
description: Recommend and document an architecture and technology stack from reviewed requirements and an existing project repository before implementation begins.
---

# Architecture Planning

Use this skill after the requirements interview has produced reviewed functional and non-functional requirements, and before implementation work begins. It helps the user choose an architecture and stack that fit the actual needs of the project.

## Review the inputs

Read the repository instructions and existing project materials before recommending anything. Look for:

- reviewed functional and non-functional requirements, including confirmed items, assumptions, and open questions;
- the MVP summary, feature roadmap, dependencies, and the next feature under consideration;
- existing code, package manifests, deployment files, and conventions that may already constrain the choices;
- explicit constraints such as team experience, schedule, budget, hosting, data privacy, integrations, and operating environment.

Use the project's actual files and tools to confirm facts. Do not assume that a technology is already selected because it is familiar or common.

When the project's needs may fit the harness's preferred stack, consult `.agents/skills/preferred-stack-guide/SKILL.md` and its `references/preferred-stack.md` before making a recommendation. Treat them as orientation, not project requirements; inspect the actual repository and requirements, and recheck time-sensitive details against current official sources.

## Make a grounded recommendation

1. Identify the requirements and constraints that most affect architecture. Map each important choice back to those inputs.
2. Recommend an architecture and technology stack sized for the project, team, hackathon timeline, existing repository, deployment needs, and incremental feature roadmap. Prefer the simplest design that supports the confirmed requirements and near-term features.
3. Describe the important components and their responsibilities, boundaries, data flow, storage, integrations, identity/access approach, and deployment/runtime model when relevant. Keep the design at the level needed to begin the next feature.
4. For significant choices, compare viable alternatives and explain tradeoffs. Make one clear recommendation; do not produce a long catalog of technologies.
5. Ask focused follow-up questions when missing or conflicting information could materially change the design. If a useful proposal can be made with an assumption, label it as provisional and state what needs confirmation.
6. Keep the architecture compatible with the agreed feature dependencies and incremental delivery plan. Do not design infrastructure for speculative future scale unless a requirement supports it.

Prioritize languages and frameworks that make errors easy for AI-assisted review to detect and explain. Consider static typing, static analysis, compiler and linter diagnostics, type-aware tooling, and automated checks. When TypeScript and JavaScript both fit the requirements and repository, evaluate TypeScript first. Treat this as a preference, not a fixed rule: team familiarity, existing project conventions, deployment constraints, or other requirements can justify another choice. Explain the reason for that choice.

As a default preference across projects handled by this harness, evaluate TypeScript for application code, Next.js for frontend applications, NestJS for backend services, PostgreSQL for relational persistence, Prisma ORM for database access, and pnpm as the package manager. Recommend this combination when it fits the confirmed requirements, repository, team, deployment environment, and current compatibility. These are defaults to evaluate, not mandatory choices: if a project has no frontend or backend, does not need relational persistence, already uses a compatible stack, or has constraints that favor another technology, mark irrelevant layers `Not applicable` or recommend a suitable alternative and explain the reason. Verify current compatibility and lifecycle details in official sources when they affect the recommendation.

When recommending a specific technology, provider, version, hosting option, or security capability whose current status could affect the choice, verify current details in authoritative primary sources such as official documentation. Explain relevant compatibility or lifecycle concerns and cite the sources used. Do not rely on memory for changing product specifications, support status, or pricing.

## Record decisions

Use `ARCHITECTURE.md` by default. If the repository already has an architecture document or decision-record convention, follow it and avoid duplicating content. Keep the record concise and focused on decisions that affect implementation.

Include the relevant sections:

- project context and architecture drivers;
- recommended architecture, components, boundaries, and important data flows;
- a dedicated Technology Stack section with concrete technology names for each relevant layer, its role, status, rationale, and meaningful alternatives;
- identity, permissions, privacy, data storage, integrations, and deployment/runtime decisions when relevant;
- assumptions and open decisions;
- relationship to the feature roadmap and prerequisites.

Mark each material decision as `Proposed`, `Confirmed`, or `Open`. A recommendation remains `Proposed` until the user confirms it. Record the reason and requirement or constraint behind each important choice. Do not fill gaps with invented requirements or unsupported quality targets.

In the Technology Stack section, give one coherent concrete stack recommendation rather than only naming categories or listing alternatives. Use a table with columns such as `Layer`, `Technology`, `Role`, `Status`, and `Rationale`. Name the actual language/runtime, application framework, data store, API or integration approach, authentication approach, and deployment platform when they apply. Mark irrelevant layers `Not applicable`. For an unresolved but necessary layer, provide a concrete provisional recommendation, mark it `Open` or `Proposed`, and state what must be confirmed. List alternatives separately with their tradeoffs; alternatives do not replace the recommended stack.

## Planning boundary

This skill produces and reviews architecture documentation. It does not implement application code, install dependencies, create infrastructure, or change runtime configuration. Approval of an architecture recommendation is not implementation approval. Follow the repository's feature-by-feature specification and approval process before changing product code.
