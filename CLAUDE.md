# CLAUDE.md — CoSAI TSC Repository

## Project Overview

This is the **Coalition for Secure AI (CoSAI) Technical Steering Committee** repository, an [OASIS Open Project](https://www.oasis-open.org/open-projects/). It contains policy documents, meeting minutes, and research publications on AI security — primarily focused on agentic systems.

- **License**: CC-BY 4.0 (documentation), Apache 2.0 (code)
- **Primary branch**: `main`
- **PR target**: always `main`

## Key Documents

| File | Description |
|------|-------------|
| `the-future-of-agentic-security.md` | Primary research paper — "From Chatbots to Autonomous Swarms". Narrative-driven analysis of multi-agent security using a 2 a.m. incident response scenario. |
| `the-future-of-agentic-security.pdf` | PDF rendering of the above paper |
| `security-principles-for-agentic-systems.md` | Security principles for agentic AI systems |
| `intro-agentic-security-principles.md` | Introduction to agentic security principles |
| `tsc-meeting-minutes/` | Weekly TSC meeting notes (YYYY-MM-DD.md format) |
| `working-documents/` | Presentations and workstream briefs |

## Paper Structure (the-future-of-agentic-security.md)

The paper follows a repeating pattern for each scenario phase:

1. **Narrative section** — describes what happens in the incident scenario
2. **Mermaid sequence diagram** — visualizes the interaction
3. **Blockquote analysis section** containing:
   - Architectural observations (bold header with `>>`)
   - Adversarial Threat Modeling
   - Implied Access & Entitlements
   - Addressing the Challenges: Infrastructure & Telemetry Upgrades
   - Research Problems (Open Challenges)
   - SVG diagram reference

### Scenario Phases
1. **The 2 A.M. Incident** — autonomous activation, event-driven NHIs
2. **The Agent That Asked for Help** — agent-to-agent delegation via natural language
3. **Who Owns This Code?** — swarm expansion, knowledge retrieval
4. **The Human on the Loop** — CI/CD boundary, GitOps enforcement
5. **Everyone in the Channel** — ADR (Agent Detection and Response), oversight agents

## Diagrams (`diagrams/`)

Research problem visualizations rendered as Graphviz DOT files and SVGs:

| DOT source | SVG output | Topic |
|------------|------------|-------|
| `research-privilege-identity.dot` | `research-privilege-identity.svg` | NHI Identity Binding, Provable IPI Robustness |
| `research-privilege-identity-v2.dot` | `research-privilege-identity-v2.svg` | Semantic Mosaic Effect, Dynamic Context Impersonation |
| `research-authorization-attestation.dot` | `research-authorization-attestation.svg` | Intent-Based Authorization, Inter-Agent Health Attestation |
| `research-control-boundaries.dot` | `research-control-boundaries.svg` | State Drift, Automation Bias, GitOps Enforcement |
| `research-edr-oversight.dot` | `research-edr-oversight.svg` | Semantic Telemetry, Low-Latency Intent Parsing |

- DOT files use `neato -n` layout with `pos` attributes for fixed positioning
- Render command: `neato -n -Tsvg input.dot -o output.svg`
- Style conventions: Montserrat font, handDrawn look, highlighted nodes use `#fff9c4` fill with `#f9a825` border
- Four research categories: Identity & Trust Boundaries, Cognitive Security & Data, Observability & Telemetry, State Operations & UX

## Key Concepts & Terminology

- **NHI** — Non-Human Identity (autonomous agents operating as identities)
- **IPI** — Indirect Prompt Injection
- **ADR** — Agent Detection and Response (vs traditional EDR)
- **AitM** — Orchestrator-in-the-Middle attack
- **JIT Upscoping** — Just-In-Time privilege elevation
- **Dynamic Contextual Downscoping** — auto-shrinking token privileges based on context toxicity
- **Semantic Smurfing** — splitting malicious intent across multiple benign requests
- **EaC** — Everything-as-Code (policy, infra, routing as Git PRs)

## Contribution Conventions

- Branch naming: `feature/`, `codebugfix/`, `languagefix/`, `release/`
- Commit messages: complete the sentence "This commit does ..."
- Rebase `main` before opening PRs, and again before merging
- Mermaid diagrams use `handDrawn` look and `neutral` theme
- SVG references in markdown use `<!--{width=55%}-->` comment for PDF rendering
- Page breaks for PDF use `<!--\newpage-->` comment
