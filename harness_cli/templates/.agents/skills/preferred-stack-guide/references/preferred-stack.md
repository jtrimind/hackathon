# Preferred Stack: Practical Project Guide

**Reference checked:** 2026-11-03
**Scope:** A starting point for projects handled by this harness. It is a preference, not a mandate. Recheck version, support, compatibility, and setup details before planning or scaffolding a real project.

## Recommended shape

For a service that needs a separate web frontend and backend API:

```text
Browser
  │ HTTPS / versioned API contract
  ▼
Next.js web app (UI, rendering, browser-facing concerns)
  │ server-side API calls where appropriate
  ▼
NestJS API (authentication/authorization, validation, business rules)
  │ Prisma ORM
  ▼
PostgreSQL
```

Keep the database private to the API. The browser should not connect to PostgreSQL. Keep business rules in NestJS so a second client (mobile, automation, or another frontend) can use the same API. Next.js Server Components can call the API server-side; avoid calling a Next.js Route Handler from a Server Component merely to proxy back into the same app. Use Route Handlers for a deliberate browser-facing backend-for-frontend concern, such as a thin proxy, webhook, or cookie/session boundary. They do not replace a dedicated backend when the project needs its own domain/API boundary.

Suggested pnpm workspace layout when a monorepo fits:

```text
project/
├─ apps/
│  ├─ web/                 # Next.js + TypeScript
│  └─ api/                 # NestJS + TypeScript + Prisma
├─ packages/
│  └─ api-contract/        # optional API schema / generated client
├─ pnpm-workspace.yaml
└─ package.json
```

Start with `apps/web` and `apps/api`. Add `packages/api-contract` only if sharing or generating an API contract provides value. Share API schemas or generated client types, not Prisma's internal database models. Runtime validation is still required at network boundaries because TypeScript types disappear at runtime.

## Technology roles and fit

| Technology | Role in the recommended shape | Good fit when | Reconsider when |
|---|---|---|---|
| TypeScript | Application language for web and API | Static checking and shared developer vocabulary help a team maintain a multi-layer app | A required platform, library, or team's constraints make another language clearly better |
| Next.js | React web application, routing, rendering, and browser-facing server features | The product needs a full-featured React web app, server rendering, or its integrated routing model | The UI is static/simple, uses another frontend, or a separate backend-for-frontend is unnecessary overhead |
| NestJS | Modular Node.js API and backend application framework | A distinct API, domain modules, dependency injection, guards, validation, or several backend integrations are useful | The app is small enough that a framework API in Next.js or a lighter server is simpler |
| PostgreSQL | Relational system of record | Data has relationships, constraints, transactions, or query needs that fit a relational database | Data shape or hosting constraints favor a different store; verify the data model first |
| Prisma ORM | Typed data access and schema/migration workflow between API code and PostgreSQL | TypeScript-oriented model/query tooling helps the team move quickly | Advanced SQL, unsupported features, operational constraints, or team expertise favor SQL-first access or another ORM |
| pnpm | Package manager; optional workspace manager for the repo | Reproducible lockfile installs and a shared multi-package workspace are useful | Repository policy, tooling, or deployment systems require another package manager |
| Jest | Default unit and integration test runner for TypeScript web/API projects | A consistent test runner across application packages is useful | A framework's official guidance or an existing toolchain favors another runner; check current framework guidance before choosing |

These layers are related but not interchangeable: TypeScript checks code before runtime; Next.js serves the web experience; NestJS owns the backend API and business rules; PostgreSQL stores durable relational data; Prisma translates between typed application code and the database; pnpm installs and links packages.

## Compatibility and release checks

Compatibility details checked against official sources on **2026-11-02**:

- **Node.js:** Use a currently supported LTS line that satisfies every selected framework's minimum. On the check date, Node.js 24 and 26 are listed as LTS; Node.js 27 is Alpha. Prefer Node.js 24 as a conservative common baseline and recheck the release table and each framework's requirements before creating the project.
- **Next.js:** The current App Router getting-started path scaffolds TypeScript by default when recommended settings are selected. Check its current Node.js floor and hosting/runtime requirements.
- **NestJS:** Current docs recommend the latest Active LTS line. Nest CLI generators have higher Node.js minimums than merely running an application, so validate the generator requirement before scaffolding.
- **Prisma ORM:** Prisma ORM 8 is currently a release candidate and has breaking workflow/API changes from Prisma ORM 7. Prisma ORM 7 remains supported. For a conservative production-oriented start, explicitly choose the stable line and follow its matching docs; use a release candidate only when the project accepts pre-release risk. Check whether the CLI, client/library, adapter, and generator packages must align for the chosen major.
- **PostgreSQL:** PostgreSQL 18 is the current major release; each major has a finite support window. Choose a supported major compatible with the selected Prisma release and hosting provider, and plan routine minor updates.
- **pnpm:** pnpm 12 is the current line; the official compatibility table lists support on Node.js 24 and 26. Record the package manager version in the project's `packageManager` field and commit `pnpm-lock.yaml` so local and CI installs use the same tool and dependency resolution. The field pins a version for package-manager-aware tooling; it does not make a missing `pnpm` executable available on PATH. Verify both `node --version` and `pnpm --version` in the terminal that will run the project. Follow the official installation page for the OS, and if installation is unavailable, use a documented ephemeral runner such as `npx --package pnpm@<version> -- pnpm --version` rather than assuming the command exists.
- **Workspace:** A pnpm workspace is declared by `pnpm-workspace.yaml`. By default, a workspace shares one lockfile at its root. After running a framework generator inside a workspace, inspect its output for nested `pnpm-workspace.yaml` or `pnpm-lock.yaml` files; consolidate them under the intended workspace root unless the project deliberately uses a nested independent workspace. Workspace linking and dependency protocols can make local package relationships explicit. Monorepo benefits must justify the added shared tooling and deployment configuration.

Release and minimum-version facts change. Do not copy the values above as permanent requirements. Check the current support and compatibility pages linked below when planning a project.

## Practical setup and delivery order

1. **Confirm the architecture first.** Decide whether the product needs both a distinct web app and API, whether it is a monorepo, where it will run, and what identity, privacy, data residency, and availability constraints apply.
2. **Choose a supported Node.js LTS and pnpm version together.** Confirm the chosen Node.js line meets Next.js, NestJS CLI, Prisma, and pnpm requirements. Pin the package manager in `package.json` and commit the lockfile.
3. **Create the workspace only if useful.** Add `pnpm-workspace.yaml` with `apps/*` and (if needed) `packages/*`. Set up root scripts and shared lint/type-check conventions only to the extent needed by both apps.
4. **Scaffold the web app.** Use the official Next.js App Router starter and TypeScript options. Keep UI, rendering, and browser-facing concerns in `apps/web`.
5. **Scaffold the API.** Use the current NestJS starter or a current official integration template that fits the workspace. Keep HTTP controllers thin; organize domain behavior into modules/services. Select and document REST/OpenAPI or another API contract based on consumers.
6. **Model and connect data.** Select a supported PostgreSQL release/provider. Add Prisma using instructions for the selected Prisma major. Keep credentials in environment/secret management, validate configuration at startup, generate migrations through the chosen workflow, and review migrations before applying them.
7. **Connect the web app to the API.** Define request/response schemas and validate untrusted input in the API. Configure local origins, API base URLs, authentication, CORS/cookies, and CSRF protections according to the deployment topology. Do not expose database credentials to the browser.
8. **Add delivery checks.** At minimum, define repeatable install, format/lint, TypeScript check, unit/integration check, and production build commands. Use Jest as the preferred unit/integration test runner by default. For React UI tests, pair it with React Testing Library; keep end-to-end testing as a separate tool decision. Check current framework guidance and configure Jest for the selected framework and TypeScript setup. Run database migrations as a deliberate deployment step and verify the rollback/backup expectations.
9. **Choose hosting after runtime needs are known.** Check support for Node.js LTS, long-running NestJS processes, PostgreSQL connection pooling, secrets, migrations, and background work. Avoid choosing providers from this guide alone.

For a local manual walkthrough, keep each required development server running in its own terminal and report the exact URL and port. Opening `localhost` will fail if the relevant server process has stopped or is listening on another port.

### Read-only database demo

When the goal is to prove that the application reads database contents, seed a small, deterministic sample set and display it without adding write operations. Make seeding safe to rerun (for example, insert only when the table is empty or use a stable upsert key); add a NestJS GET endpoint that reads through Prisma; then render the returned records in Next.js. Verify the database endpoint response and the browser view. Keep this flow distinct from a real user-data feature, which needs its own write, validation, authorization, and migration design.

## Common pitfalls to check

- **Two backends doing the same work:** Decide which layer owns business rules. Keep Next.js Route Handlers thin if NestJS is the primary API.
- **Trusting TypeScript at HTTP boundaries:** Validate request data at runtime; static types do not validate JSON sent by a browser or external client.
- **Leaking data-layer concerns:** Return API DTOs, not raw Prisma records. Avoid importing database models into the web app as its API contract.
- **Mismatched versions:** Keep Prisma packages/adapters on compatible versions and confirm the selected Node.js version meets all scaffolder and runtime floors.
- **Generated client drift:** Run the chosen Prisma generation/emission step reliably in local development and CI/builds; follow the selected major's guidance.
- **Migration surprises:** Review generated SQL/migrations, use separate development and production credentials, back up important data, and choose a deployment order that avoids incompatible app/schema changes.
- **Connection exhaustion:** Serverless functions and multiple app replicas can multiply database connections. Use the provider's supported pooling approach and verify Prisma adapter requirements.
- **Overbuilt monorepo:** A workspace adds root configuration, task orchestration, and deployment decisions. Start with separate packages or repositories if sharing is not useful.
- **Nested workspace created by a scaffold:** Generators may write a workspace file or lockfile inside `apps/web`. Check generated files and install output; with the usual shared-lockfile workspace, keep package discovery and the lockfile at the repository root.
- **pnpm executable missing:** `packageManager` metadata is not a substitute for installing/enabling pnpm. A shell may also have stale PATH state after installation; open a fresh terminal and check `pnpm --version` before starting scripts.
- **pnpm installation approvals:** Recent pnpm versions can separately gate dependency build scripts and agent skills. Review what each package requests. Use `pnpm approve-builds` for necessary build scripts and `pnpm approve` for requested capabilities/skills where supported; these approvals are distinct. Approve only packages needed by the project, and do not use `--all` as a blanket workaround. After approval, rerun install and verify generation/build steps.
- **PostgreSQL 18 Docker volume path:** The official `postgres` image changed its volume layout in PostgreSQL 18. For 18+, mount persistent storage at `/var/lib/postgresql`; for 17 and below, the documented data mount is `/var/lib/postgresql/data`. Check the image's version-specific instructions before copying compose examples, or data may not persist as expected.
- **NestJS injection with tsx/esbuild:** `tsx` transpilation does not emit TypeScript decorator metadata for Nest's implicit constructor-token lookup. In that setup, use explicit `@Inject(ProviderToken)` on injected constructor parameters (including PrismaService) as shown by Prisma's current NestJS guide.
- **Demo scope grows into CRUD:** A preloaded-data walkthrough only needs a reliable read path. Do not add mutations unless they are part of the approved requirement.
- **Assuming one deployment shape:** Next.js server rendering and a long-running NestJS API may have different runtime needs. Confirm platform support before selecting a host.

## Official sources

Existing compatibility links were checked on **2026-11-02**; testing references were checked on **2026-11-03**. Recheck before using version numbers, setup commands, or support statements.

### Languages and frameworks

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — language and type-system concepts.
- [Next.js App Router: Getting Started](https://nextjs.org/docs/app/getting-started) — current starter and project structure.
- [Next.js Backend for Frontend guide](https://nextjs.org/docs/app/guides/backend-for-frontend) — Route Handler scope, caveats, and security notes.
- [NestJS First Steps](https://docs.nestjs.com/first-steps) — Node.js requirements, TypeScript, scaffolding, modules, and adapters.
- [Node.js Releases](https://nodejs.org/en/about/previous-releases) — current release and LTS status.

### Database, ORM, and package manager

- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html) — relational concepts, SQL, and database basics.
- [PostgreSQL Versioning Policy](https://www.postgresql.org/support/versioning/) — support windows, releases, and upgrade expectations.
- [Prisma ORM Release Status](https://www.prisma.io/docs/orm/release-status) — stable/pre-release status and major-version transitions.
- [Prisma ORM with NestJS](https://www.prisma.io/docs/guides/frameworks/nestjs) — current NestJS integration path.
- [Prisma ORM with PostgreSQL](https://www.prisma.io/docs/orm/v7/overview/databases/postgresql) — PostgreSQL connector; use the documentation section matching the selected ORM major.
- [pnpm Installation and Compatibility](https://pnpm.io/installation) — supported pnpm and Node.js lines.
- [pnpm Workspaces](https://pnpm.io/workspaces) — workspace setup and local package linking.
- [pnpm approve-builds](https://pnpm.io/cli/approve-builds) — approval for dependency installation build scripts.
- [pnpm permissions](https://pnpm.io/cli/permissions) — pnpm 12 capability and agent-skill approvals.
- [PostgreSQL Official Docker Image](https://hub.docker.com/_/postgres) — image-specific environment and persistent-volume paths, including the PostgreSQL 18 change.
- [pnpm Settings](https://pnpm.io/settings) — workspace and package-manager configuration.
