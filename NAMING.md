# Naming Onomly

This document records how the product name **Onomly** was selected, using a 6-phase professional naming process (brief → generate → shortlist → validate → decide → launch). It is preserved so future rebrands or sub-product naming can follow the same evidence-led approach.

## Selected Name

| Property | Value |
|---|---|
| **Name** | Onomly |
| **Pronunciation** | /ˈɒn.əm.li/ — "ON-um-lee" |
| **Typology** | Real-word blend (onomastics + "-ly") |
| **Length** | 7 characters, 3 syllables |
| **Tagline** | *"Name what's next."* |
| **Primary domain** | onomly.com (available) |
| **Console command** | `onomly` |

## Phase 0 — Brief

**Project:** An AI agent orchestration and brand-naming engine (Python). It generates brand-name candidates via LLM, validates them across domain (RDAP), trademark, and social-handle availability, with SQLite caching, rate limiting, and retry-with-backoff.

**Target markets:** global SaaS developers, brand strategists / naming agencies, indie hackers, enterprise internal-tooling teams.

**Brand personality:** intelligent, pragmatic, precise, modern, trustworthy.

**Selection criteria (scored 1–5):** distinctiveness, memorability, pronounceability, domain availability, trademark clearance, social-handle availability, relevance, brevity, brandability, future-proofing.

**Constraints:** must not collide with internal module name `launch_engine`; avoid saturated terms (launch, engine, orion, nova, apex, vertex, synth, nexus); avoid negative meanings in English/Turkish/German; prefer ≤10 chars; must read as a real or near-real word (no fully invented syllables).

## Phase 1 — Generation (10 lenses)

Candidates were generated across all ten typology lenses: real words, metaphorical, compound, blended, abstract/coined, foreign-language, people/place/myth, modifier+noun, phrase/tagline-born, sound-symbolic.

**First pass (rejected):** A fully coined abstract name, **KLYDRIX**, was the initial winner. User feedback: *"klydrix çok uydurma oldu"* ("klydrix is too made-up / invented"). Lesson logged: the product audience reads a coined string as artificial, so the final name must be grounded in a real word or obvious word-blend.

**Second pass (natural typologies):** real words (compass, prism, beacon, keystone, lodestar, augur, cipher, lexicon, eponym, moniker, sobriquet), and real-word + naming-suffix compounds (namekit, brandkit, namelab, monikerly, onomly, nameworks).

## Phase 2 — Shortlist

Real English words were uniformly **taken** on `.com` + X + GitHub (only `.io` free). The viable natural candidates were word-blends with `.com` still open:

| Name | Typology | .com | Notes |
|---|---|---|---|
| **onomly** | Blend (onomastics + -ly) | ✅ | Real-word root, friendly suffix |
| monikerly | Blend (moniker + -ly) | ❌ (.com taken) | Strong but squatted |
| nameworks | Compound | ❌ (.com taken) | GitHub also taken |

## Phase 3 — Validation Gates

Live checks (RDAP, HTTP HEAD, GitHub/npm/PyPI APIs, web search):

| Candidate | .com | .io | .ai | X | IG | LI | GitHub | npm | PyPI |
|---|---|---|---|---|---|---|---|---|---|
| **onomly** | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| monikerly | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| nameworks | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |

- **Trademark:** no conflicts found for "Onomly" via web search. USPTO TESS requires authenticated access — manual review recommended before filing.
- **Linguistic:** clean in English, Turkish, and German. "Onomly" derives from *onomatics* / *onomastics* (the study of names) — directly relevant to a naming tool, not a random coinage. No negative homophones; no untypable characters.

## Phase 4 — Decision

**Onomly** selected:

1. **Real-word root** — rooted in *onomastics* (the study of names), so it is semantically self-describing for a naming engine. No "uydurma" feel.
2. **All critical domains open** — `.com` / `.io` / `.ai` all available (the scarce asset); GitHub + PyPI free.
3. **Pronounceable & memorable** — ON-um-lee, 3 syllables, obvious spelling.
4. **Brandable** — friendly "-ly" suffix softens the academic root into a product name.
5. **No trademark conflicts** found in web search.

**Rejected:** monikerly and nameworks — both have `.com` already registered (the dealbreaker for a primary domain).

## Phase 5 — Brand Identity

| Token | Hex | Usage |
|---|---|---|
| primary | `#1A120B` | background / deep UI |
| accent | `#C9A227` | highlights, logo accent |
| code-green | `#5C7A6E` | syntax highlights |
| text | `#EDE1C8` | primary text on dark |
| danger | `#6B1E23` | error states |

**Voice:** precise, confident, no fluff. Lead with the answer; never oversell. CLI/command references use lowercase monospace (`onomly generate-names`); the brand name in prose uses `Onomly`.

**Logo concept:** a terminal-window monogram — `O|NO` on the left (sidebar) and `> MLY$` on the right (command prompt), where `>` marks the moment of creation.

## Open Launch Actions (not yet executed)

These require payment / manual authorization and were **not** performed during naming:

- [ ] Register `onomly.com`, `onomly.io`, `onomly.ai`
- [ ] Claim `@onomly` on X/Twitter (currently taken — use a handle variant or acquire)
- [ ] Create GitHub org `onomly`
- [ ] Publish `onomly` on PyPI and npm
- [ ] File USPTO trademark for "Onomly" (Class 9 software, Class 42 SaaS)
