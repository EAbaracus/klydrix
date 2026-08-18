# Naming KLYDRIX

This document records how the product name **KLYDRIX** was selected, using a 6-phase professional naming process (brief → generate → shortlist → validate → decide → launch). It is preserved so future rebrands or sub-product naming can follow the same evidence-led approach.

## Selected Name

| Property | Value |
|---|---|
| **Name** | KLYDRIX |
| **Pronunciation** | /ˈklaɪ-drɪks/ — "KLY-driks" |
| **Typology** | Abstract / Coined |
| **Length** | 7 characters, 2 syllables |
| **Tagline** | *"Name what's next."* |
| **Primary domain** | klydrix.com (available) |
| **Console command** | `klydrix` |

## Phase 0 — Brief

**Project:** An AI agent orchestration and brand-naming engine (Python). It generates brand-name candidates via LLM, validates them across domain (RDAP), trademark, and social-handle availability, with SQLite caching, rate limiting, and retry-with-backoff.

**Target markets:** global SaaS developers, brand strategists / naming agencies, indie hackers, enterprise internal-tooling teams.

**Brand personality:** intelligent, pragmatic, precise, modern, trustworthy.

**Selection criteria (scored 1–5):** distinctiveness, memorability, pronounceability, domain availability, trademark clearance, social-handle availability, relevance, brevity, brandability, future-proofing.

**Constraints:** must not collide with internal module name `launch_engine`; avoid saturated terms (launch, engine, orion, nova, apex, vertex, synth, nexus); avoid negative meanings in English/Turkish/German; prefer ≤10 chars, ≤2 syllables.

## Phase 1 — Generation (10 lenses)

Candidates were generated across all ten typology lenses: real words, metaphorical, compound, blended, abstract/coined, foreign-language, people/place/myth, modifier+noun, phrase/tagline-born, sound-symbolic. 16 candidates advanced to scoring.

## Phase 2 — Shortlist

Scored on the 10 criteria. Top tier:

| Name | Typology | Avg |
|---|---|---|
| **KLYDRIX** | Coined | **4.2** |
| **VYLDRANX** | Coined | 4.1 |
| **MYRLIXIS** | Blended | 4.0 |
| sylqen | Coined | 3.6 |
| sylphari | Coined | 3.5 |

## Phase 3 — Validation Gates

All checks performed with live tooling (RDAP, HTTP HEAD, GitHub/npm/PyPI APIs, web search):

| Candidate | .com | .io | .ai | X | IG | LI | GitHub | npm | PyPI |
|---|---|---|---|---|---|---|---|---|---|
| **klydrix** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| vyldranx | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| myrlixis | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| sylqen | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| sylphari | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |

- **Trademark:** no conflicts found for KLYDRIX / VYLDRANX / MYRLIXIS via web search. USPTO TESS requires authenticated access — manual review recommended before filing.
- **Linguistic:** all three finalists are clean in English, Turkish, and German (no negative homophones; no non-typable characters on standard Turkish Q-keyboard layouts, unlike earlier `q…` candidates).

## Phase 4 — Decision

**KLYDRIX** selected as the winner:

1. Shortest of the finalists (7 chars, 2 syllables) — easiest to type and remember.
2. Sharp "K" onset reads as technical/precise; "drix" echoes "index" without being derivative.
3. All critical domains (.com/.io/.ai) and the X/Twitter handle are available.
4. No trademark conflicts found; GitHub/npm/PyPI all open.
5. Pronounceable and brandable — strong in monospace terminal UIs.

**Runner-up rationale:** VYLDRANX has a less natural "vy" onset in English; MYRLIXIS reads slightly more "personal" (myr- = "my").

## Phase 5 — Brand Identity

| Token | Hex | Usage |
|---|---|---|
| primary | `#1A120B` | background / deep UI |
| accent | `#C9A227` | highlights, logo accent |
| code-green | `#5C7A6E` | syntax highlights |
| text | `#EDE1C8` | primary text on dark |
| danger | `#6B1E23` | error states |

**Voice:** precise, confident, no fluff. Lead with the answer; never oversell. CLI/command references use lowercase monospace (`klydrix generate-names`); the brand name in prose uses `Klydrix` or `KLYDRIX`.

**Logo concept:** a terminal-window monogram — `K|LY` on the left (sidebar) and `> DRIX$` on the right (command prompt), where `>` marks the moment of creation.

## Open Launch Actions (not yet executed)

These require payment / manual authorization and were **not** performed during naming:

- [ ] Register `klydrix.com`, `klydrix.io`, `klydrix.ai`
- [ ] Claim `@klydrix` on X/Twitter
- [ ] Create GitHub org `klydrix`
- [ ] Publish `klydrix` on PyPI and npm
- [ ] File USPTO trademark for "KLYDRIX" (Class 9 software, Class 42 SaaS)
