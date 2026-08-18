"""Trademark availability checker (stub)."""

from __future__ import annotations

from .base import AdapterPolicy, ValidationResult, ValidationStatus


class TrademarkAdapter:
    """Stub trademark checker."""

    version = "1.0.0"
    policy = AdapterPolicy(
        rate_limit_per_minute=10,
        cache_ttl_seconds=3600,  # 1 hour
        timeout_seconds=30.0,
    )

    async def validate(self, trademark: str) -> ValidationResult:
        """Check if a trademark is available.

        This is a stub implementation that always returns UNVERIFIABLE
        because real trademark checking requires paid APIs.

        Args:
            trademark: The trademark to check.

        Returns:
            ValidationResult with status UNVERIFIABLE and a manual_review_url.
        """
        # Normalize trademark: strip whitespace
        trademark = trademark.strip()
        if not trademark:
            return ValidationResult(
                status=ValidationStatus.UNVERIFIABLE,
                error="Empty trademark",
            )

        # Provide a manual review URL (using USPTO TESS as an example)
        manual_review_url = (
            "https://tmsearch.uspto.gov/bin/gate.exe?f=searchss&state=4801:yfxrku.1.1"
        )

        return ValidationResult(
            status=ValidationStatus.UNVERIFIABLE,
            trademark=trademark,
            details={"manual_review_url": manual_review_url},
        )
