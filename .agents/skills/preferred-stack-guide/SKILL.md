---
name: preferred-stack-guide
description: Use the harness's source-backed preferred-stack guide when planning a new TypeScript web project with Next.js, NestJS, PostgreSQL, Prisma ORM, and pnpm.
---

# Preferred Stack Guide

Use this skill alongside `architecture-planning` when the user is considering a new project that may fit the harness's preferred stack.

## Workflow

1. Read the project's reviewed requirements, repository instructions, existing code and manifests, and the reference guide at `references/preferred-stack.md`.
2. Treat the stack in the reference as a starting recommendation, not a requirement. Mark layers that do not apply as not applicable and explain justified alternatives.
3. Before making version, support, compatibility, setup-command, or hosting claims, check the linked official sources for current details. Do not assume the reference's last-verified notes are still current.
4. Fit the architecture to the actual need. For a conventional service with distinct frontend and backend, consider Next.js as the web application and NestJS as the API, with PostgreSQL accessed by the backend through Prisma ORM. Use pnpm workspaces when a monorepo benefits the project; do not introduce one without a reason.
5. For a manual demo whose goal is to show existing database values, prefer an explicitly read-only path: deterministic sample rows, a NestJS read endpoint, and a Next.js view. Do not add create/update/delete flows unless requested.
6. Record concrete choices, roles, status, rationale, alternatives, constraints, assumptions, and open decisions in the project's architecture document, following `architecture-planning`.

## Planning boundaries

- Do not install dependencies, generate an application, provision a database, or change runtime configuration during architecture planning.
- Do not present a type shared by TypeScript as proof that an HTTP payload is valid. Define and validate API contracts at runtime.
- Keep database access and business rules behind the NestJS API when both Next.js and NestJS are selected. Next.js can render the UI and make server-side requests to the API; use Route Handlers as a thin backend-for-frontend only when they solve a concrete need.
- Revisit source links and release status whenever the guide is used. Update the guide's verification date and notes only when maintaining this reference as an approved feature.
