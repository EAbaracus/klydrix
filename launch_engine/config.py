"""Persistent user config for Onomly (chosen LLM model, etc.).

Stored as JSON at ``<config_dir>/onomly/config.json``. The config dir follows the
XDG base-directory spec on Linux and uses the equivalent ``AppData\\Local`` path on
Windows. Secrets are never written here — only the model selection; API keys come
from the environment or 9router.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from launch_engine.models import DEFAULT_MODEL, ModelEntry, find_by_id


def config_dir() -> Path:
    """Return the platform-appropriate config directory for Onomly.

    Honors ``ONOMLY_CONFIG_DIR`` for testing / portable installs, then follows the
    XDG base-directory spec on Linux and the ``AppData\\Local`` path on Windows.
    """
    override = os.environ.get("ONOMLY_CONFIG_DIR")
    if override:
        return Path(override)
    if os.name == "nt":
        base = Path.home() / "AppData" / "Local"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "onomly"


def config_path() -> Path:
    return config_dir() / "config.json"


@dataclass
class OnomlyConfig:
    llm_provider: str = DEFAULT_MODEL.provider
    llm_model: str = DEFAULT_MODEL.model
    configured: bool = False

    @property
    def model_id(self) -> str:
        return f"{self.llm_provider}/{self.llm_model}"

    def to_entry(self) -> ModelEntry:
        entry = find_by_id(self.model_id)
        if entry is None:
            # Unknown / custom selection — return a minimal entry so callers work.
            return ModelEntry(
                provider=self.llm_provider,
                model=self.llm_model,
                label=f"{self.llm_provider}/{self.llm_model}",
                needs_key=(self.llm_provider not in ("9router", "ollama")),
            )
        return entry


def load_config(path: Path | None = None) -> OnomlyConfig:
    """Load config from disk, falling back to defaults if absent or invalid."""
    p = path or config_path()
    if not p.exists():
        return OnomlyConfig()
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        return OnomlyConfig(
            llm_provider=data.get("llm_provider", DEFAULT_MODEL.provider),
            llm_model=data.get("llm_model", DEFAULT_MODEL.model),
            configured=bool(data.get("configured", False)),
        )
    except (json.JSONDecodeError, OSError):
        return OnomlyConfig()


def save_config(cfg: OnomlyConfig, path: Path | None = None) -> Path:
    """Persist config to disk, creating the directory if needed."""
    p = path or config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(asdict(cfg), f, indent=2)
    return p
