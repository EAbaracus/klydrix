# KLYDRIX

> AI brand-naming and validation engine — generate, score, and clear candidate names across domain, trademark, and social channels.

KLYDRIX (internal package: `launch_engine`) is a Python framework that turns a naming brief into a defensible shortlist. It generates brand-name candidates with an LLM, applies phonetic and semantic filters, scores each candidate, and then validates availability through pluggable adapters (RDAP domain lookup, trademark gateway, social-handle checks) with SQLite caching, token-bucket rate limiting, and retry-with-backoff.

The brand name **KLYDRIX** itself was produced by running this engine end-to-end — see [`NAMING.md`](NAMING.md) for the full naming brief, shortlist, validation evidence, and decision record.

## Features

- **Divergent → Convergent generation** — LLM generates diverse candidates across 8 name typologies, then scores and ranks them.
- **Phonetic filtering** — syllable, length, and avoided-sound constraints applied mid-pipeline.
- **Pluggable validation adapters** — Domain (RDAP), Trademark (manual-review gateway), and Social (X / Instagram / LinkedIn).
- **Resilient pipeline** — per-adapter rate limiting (token bucket), exponential-backoff retry on transient errors, and TTL-based SQLite caching.
- **CLI** — `generate-names`, `validate`, `cache`, and `adapters` commands with table / JSON / CSV output.
- **Async-first** — built on `asyncio` throughout; `pydantic` models for all I/O contracts.

## Installation

```bash
pip install klydrix
```

For development:

```bash
git clone https://github.com/EAbaracus/klydrix.git
cd klydrix
pip install -e ".[dev]"
```

> **Note on package naming:** the importable package is `launch_engine` (kept stable to avoid breaking the existing module graph). The installed console script and published distribution name is `klydrix`.

## Quick Start

### CLI

```bash
# Generate candidates from a brief
klydrix generate-names \
  --project-codename "my_saas" \
  --description "AI agent orchestration platform" \
  --target-markets "USA,EU" \
  --industry "Technology" \
  --llm-provider ollama \
  --llm-model qwen3:14b \
  --output-format table

# Validate a previously generated candidate file
klydrix validate \
  --candidates-file candidates.json \
  --target-markets "USA,EU" \
  --industry "Technology" \
  --output-format json
```

### Python

```python
import asyncio
from launch_engine.engine import LaunchEngine
from launch_engine.modules.naming.brief import NamingBrief

async def main():
    engine = LaunchEngine(
        llm_provider="ollama",
        llm_model="qwen3:14b",
        cache_db_path="klydrix_cache.db",
    )
    brief = NamingBrief(
        project_codename="my_saas",
        description="AI agent orchestration platform",
        target_markets=["USA", "EU"],
        industry="Technology",
        candidate_count=10,
    )
    candidates, results = await engine.run_full_pipeline(brief)
    for c in candidates.candidates:
        print(c.name, c.typology, c.internal_assessment.score)

asyncio.run(main())
```

## Architecture

KLYDRIX follows a modular pipeline architecture:

- **Brand Naming Module** (`launch_engine/modules/naming/`) — brief parsing, divergent LLM generation, phonetic mid-filter, convergent LLM scoring.
- **LLM Adapter** (`launch_engine/llm.py`) — provider-agnostic calls via LiteLLM (ollama, openai, anthropic, 9router).
- **Validation Pipeline** (`launch_engine/validation/`) — orchestrates adapters with concurrency control, rate limiting, retry, and caching.
- **Cache Layer** (`launch_engine/cache.py`) — SQLite-backed TTL cache keyed by content hash.
- **CLI** (`launch_engine/cli/`) — Typer-based command surface.

### Data Flow

```
NamingBrief
   │
   ▼
BrandNamingModule.run()
   ├─ _divergent_generate()  → LLM → NameCandidate[]
   ├─ _midfilter()           → phonetic + avoid-term filter
   └─ _convergent_score()    → LLM → scored & ranked NameCandidateList
   │
   ▼
ValidationPipeline.validate_all()
   └─ for each (candidate, adapter): rate-limit → retry → cache → ValidationResult
```

## Development

```bash
pip install -e ".[dev]"
pytest                      # run the suite
black --check .             # formatting
ruff check .                # lint
mypy .                      # types
```

## Documentation

- [NAMING.md](NAMING.md) — how the **KLYDRIX** name was chosen (brief, shortlist, validation, decision).
- [CONTRIBUTING.md](CONTRIBUTING.md) — dev setup and PR process.

## License

Apache 2.0 — see [LICENSE](LICENSE).
