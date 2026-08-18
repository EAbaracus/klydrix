"""Validation models and enums for Launch Engine."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class ValidationStatus(str, Enum):
    """Validation status."""

    AVAILABLE = "available"
    TAKEN = "taken"
    UNVERIFIABLE = "unverifiable"
    ERROR = "error"


class Confidence(str, Enum):
    """Confidence level."""

    CONFIRMED = "confirmed"
    LIKELY = "likely"
    UNKNOWN = "unknown"


class ValidationChannel(str, Enum):
    """Validation channel."""

    DOMAIN = "domain"
    TRADEMARK_TR = "trademark_tr"
    TRADEMARK_GLOBAL = "trademark_global"
    SOCIAL_X = "social_x"
    SOCIAL_INSTAGRAM = "social_instagram"
    SOCIAL_LINKEDIN = "social_linkedin"


class Evidence(BaseModel):
    """Evidence for a validation."""

    source: str
    url: Optional[str] = None
    checked_at: datetime
    raw: Optional[dict[str, Any]] = None


class ValidationResult(BaseModel):
    """Result of a validation check."""

    target: str
    channel: ValidationChannel
    status: ValidationStatus
    confidence: Confidence
    evidence: Evidence
    candidate_id: str
    validation_id: str
    adapter_version: str
    checked_at: datetime
    manual_review_url: Optional[str] = None


class CacheEntry(BaseModel):
    """Cache entry for validation results."""

    key: str
    result: ValidationResult
    expires_at: datetime
    adapter_version: str
    policy_version: str
    created_at: datetime
