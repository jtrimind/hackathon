# Non-Functional Requirements

### NFR-001: Keep stack guidance verifiable and current
- **Statement:** Stack guidance identifies authoritative official sources and when the source information was checked; architecture planning rechecks current compatibility and lifecycle details when they could affect a recommendation.
- **Actor/context:** Users and agents relying on the preferred-stack reference during project planning.
- **Conditions and exceptions:** Stable concepts may be summarized, but changing versions, support status, compatibility, commands, and pricing must not be presented as timeless facts.
- **Acceptance or verification:** The reference includes official documentation links and a last-verified date, and the architecture-planning workflow explicitly calls for checking time-sensitive details against current primary sources.
- **Status:** Confirmed
- **Source:** User request for pre-researched reference files; existing architecture-planning workflow requiring verification of changeable technology details.

### NFR-002: Preserve the preferred stack as a default, not a mandate
- **Statement:** The guide supports project-specific decisions and does not imply that every project must use every preferred technology.
- **Actor/context:** Architecture planning across projects with differing requirements, repositories, teams, and deployment constraints.
- **Conditions and exceptions:** Irrelevant layers may be marked not applicable; alternatives may be recommended with reasons.
- **Acceptance or verification:** Guidance distinguishes default recommendations from requirements and includes conditions that could justify deviations.
- **Status:** Confirmed
- **Source:** User's prior confirmation that the named technologies are common preferences for projects handled by the harness.
