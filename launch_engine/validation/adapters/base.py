"""Base classes and protocols for validation adapters."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable


class ValidationStatus(str, Enum):
    """Validation status."""

    AVAILABLE = "available"
    TAKEN = "taken"
    UNVERIFIABLE = "unverifiable"


@dataclass
class ValidationResult:
    """Result of a validation check."""

    status: ValidationStatus
    domain: str | None = None  # for domain adapter
    trademark: str | None = None  # for trademark adapter
    social_media: str | None = None  # for social media adapter
    details: dict | None = None
    error: str | None = None


@dataclass
class AdapterPolicy:
    """Policy for an adapter."""

    rate_limit_per_minute: int
    cache_ttl_seconds: int
    timeout_seconds: float


@runtime_checkable
class ValidationAdapter(Protocol):
    """Protocol for validation adapters."""

    version: str
    policy: AdapterPolicy

    async def validate(self, value: str) -> ValidationResult:
        """Validate a value.

        Args:
            value: The value to validate (e.g., domain name, trademark, username).

        Returns:
            ValidationResult.
        """
        ...
