"""Curated LLM model catalog for Onomly.

The catalog is intentionally small and honest: every entry either routes through
9router (no user-supplied API key required) or clearly states the provider and
that an API key / env var is needed. Free-tier models are marked so first-run
users are not dropped into a paid bill by surprise.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelEntry:
    provider: str
    model: str
    label: str
    needs_key: bool = False
    free_tier: bool = False
    note: str = ""

    @property
    def id(self) -> str:
        """Canonical id Onomly uses internally (provider/model)."""
        return f"{self.provider}/{self.model}"


# Default model used when no config exists and the user has not run `onomly configure`.
DEFAULT_MODEL = ModelEntry(
    provider="9router",
    model="kc/nvidia/nemotron-3-super-120b-a12b:free",
    label="9router · Nemotron 3 Super 120B (free)",
    needs_key=False,
    free_tier=True,
    note="Routed via 9router; no API key required.",
)

MODELS: list[ModelEntry] = [
    DEFAULT_MODEL,
    ModelEntry(
        provider="9router",
        model="google/gemini-2.5-flash:free",
        label="9router · Gemini 2.5 Flash (free)",
        needs_key=False,
        free_tier=True,
        note="Routed via 9router; no API key required.",
    ),
    ModelEntry(
        provider="9router",
        model="deepseek/deepseek-chat:free",
        label="9router · DeepSeek Chat (free)",
        needs_key=False,
        free_tier=True,
        note="Routed via 9router; no API key required.",
    ),
    ModelEntry(
        provider="9router",
        model="openai/gpt-oss-120b:free",
        label="9router · GPT-OSS 120B (free)",
        needs_key=False,
        free_tier=True,
        note="Routed via 9router; no API key required.",
    ),
    ModelEntry(
        provider="ollama",
        model="qwen3:14b",
        label="Local Ollama · qwen3:14b",
        needs_key=False,
        free_tier=True,
        note="Requires a local Ollama server (http://localhost:11434).",
    ),
    ModelEntry(
        provider="openai",
        model="gpt-4o-mini",
        label="OpenAI · gpt-4o-mini",
        needs_key=True,
        free_tier=False,
        note="Requires OPENAI_API_KEY in the environment.",
    ),
    ModelEntry(
        provider="anthropic",
        model="claude-3-5-haiku-latest",
        label="Anthropic · Claude 3.5 Haiku",
        needs_key=True,
        free_tier=False,
        note="Requires ANTHROPIC_API_KEY in the environment.",
    ),
]


def find_by_id(model_id: str) -> ModelEntry | None:
    """Resolve a provider/model id to a catalog entry, if present."""
    for entry in MODELS:
        if entry.id == model_id:
            return entry
    return None


def default_entry() -> ModelEntry:
    return DEFAULT_MODEL
