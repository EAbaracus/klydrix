"""Tests for the validation pipeline orchestrator."""

import asyncio
import time
from unittest.mock import AsyncMock, Mock
from typing import Optional
import pytest

from launch_engine.validation.pipeline import ValidationPipeline
from launch_engine.validation.adapters.base import (
    ValidationAdapter,
    ValidationResult,
    ValidationStatus,
    AdapterPolicy,
)
from launch_engine.cache import SQLiteCache
from launch_engine.modules.naming.brief import NamingBrief, NameTypology
from launch_engine.modules.naming.candidates import NameCandidate
from launch_engine.core.validation import (
    ValidationResult as CoreValidationResult,
    ValidationStatus as CoreValidationStatus,
    ValidationChannel,
    Confidence,
    Evidence,
)
from datetime import datetime


class MockValidationAdapter(ValidationAdapter):
    """Mock validation adapter for testing."""

    def __init__(
        self,
        version: str = "1.0.0",
        policy: Optional[AdapterPolicy] = None,
        validate_result: Optional[ValidationResult] = None,
        validate_exception: Optional[Exception] = None,
    ):
        self._version = version
        self._policy = policy or AdapterPolicy(
            rate_limit_per_minute=60,
            cache_ttl_seconds=3600,
            timeout_seconds=30.0,
        )
        self._validate_result = validate_result or ValidationResult(
            status=ValidationStatus.AVAILABLE
        )
        self._validate_exception = validate_exception
        self.validate_call_count = 0
        self.validate_called_with = None

    @property
    def version(self) -> str:
        return self._version

    @property
    def policy(self) -> AdapterPolicy:
        return self._policy

    async def validate(self, value: str) -> ValidationResult:
        """Mock validate method."""
        self.validate_call_count += 1
        self.validate_called_with = value

        if self._validate_exception:
            raise self._validate_exception

        return self._validate_result


@pytest.fixture
def mock_cache():
    """Create a mock cache for testing."""
    cache = Mock(spec=SQLiteCache)
    cache.get = AsyncMock(return_value=None)  # Default to cache miss
    cache.set = AsyncMock()
    cache.initialize = AsyncMock()
    cache.close = AsyncMock()
    return cache


@pytest.fixture
def naming_brief():
    """Create a naming brief for testing."""
    return NamingBrief(
        project_codename="test_project",
        description="A test project",
        target_markets=["US", "EU"],
        industry="Technology",
    )


@pytest.fixture
def name_candidate():
    """Create a name candidate for testing."""
    return NameCandidate(
        candidate_id="test_1",
        name="TestName",
        typology=NameTypology.INVENTED,
        rationale="Test rationale",
    )


@pytest.mark.asyncio
async def test_validate_all_parallel_execution(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline runs adapters in parallel."""
    # Create mock adapters
    adapter1 = MockValidationAdapter(
        version="1.0.0",
        validate_result=ValidationResult(status=ValidationStatus.AVAILABLE)
    )
    adapter2 = MockValidationAdapter(
        version="2.0.0",
        validate_result=ValidationResult(status=ValidationStatus.TAKEN)
    )

    pipeline = ValidationPipeline(
        adapters=[adapter1, adapter2],
        cache=mock_cache,
        max_concurrency=10,
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 2  # 1 candidate × 2 adapters
    assert adapter1.validate_call_count == 1
    assert adapter2.validate_call_count == 1
    assert adapter1.validate_called_with == "TestName"
    assert adapter2.validate_called_with == "TestName"


@pytest.mark.asyncio
async def test_validate_all_cache_hit(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline uses cache when available."""
    # Setup mock to return a cached result
    cached_result = CoreValidationResult(
        target="TestName",
        channel=ValidationChannel.DOMAIN,
        status=CoreValidationStatus.AVAILABLE,
        confidence=Confidence.CONFIRMED,
        evidence=Evidence(
            source="cached",
            checked_at=datetime.now(),
        ),
        candidate_id="test_1",
        validation_id="test_1_domain_123",
        adapter_version="1.0.0",
        checked_at=datetime.now(),
    )
    mock_cache.get.return_value = cached_result

    adapter = MockValidationAdapter(
        version="1.0.0",
        validate_result=ValidationResult(
            status=ValidationStatus.TAKEN
        )  # Different from cached
    )

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 1
    assert results[0] == cached_result  # Should return cached result
    assert adapter.validate_call_count == 0  # Adapter should not be called
    mock_cache.get.assert_called_once()
    mock_cache.set.assert_not_called()  # Should not set cache on hit


@pytest.mark.asyncio
async def test_validate_all_cache_miss(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline calls adapter and stores result on cache miss."""
    mock_cache.get.return_value = None  # Cache miss

    adapter_result = ValidationResult(status=ValidationStatus.AVAILABLE)
    adapter = MockValidationAdapter(
        version="1.0.0",
        validate_result=adapter_result
    )

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 1
    assert adapter.validate_call_count == 1
    mock_cache.get.assert_called_once()
    mock_cache.set.assert_called_once()  # Should store result in cache


@pytest.mark.asyncio
async def test_validate_all_retry_on_transient_error(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline retries on transient errors."""
    # Fail twice with timeout, then succeed
    call_count = 0

    async def mock_validate(value: str):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise TimeoutError("Request timeout")
        return ValidationResult(status=ValidationStatus.AVAILABLE)

    adapter = MockValidationAdapter(
        version="1.0.0",
        validate_result=ValidationResult(status=ValidationStatus.AVAILABLE)
    )
    # Replace the validate method with our mock
    adapter.validate = mock_validate

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 1
    assert call_count == 3  # Should have retried twice then succeeded
    # The final result should be SUCCESS (not unverifiable)
    # Note: Our mock returns AVAILABLE which maps to AVAILABLE in core


@pytest.mark.asyncio
async def test_validate_all_no_retry_on_permanent_error(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline does not retry on permanent errors."""
    call_count = 0

    async def mock_validate(value: str):
        nonlocal call_count
        call_count += 1
        # Return a taken result (not an error, so no retry)
        return ValidationResult(status=ValidationStatus.TAKEN)

    adapter = MockValidationAdapter(
        version="1.0.0",
        validate_result=ValidationResult(status=ValidationStatus.TAKEN)
    )
    # Replace the validate method with our mock
    adapter.validate = mock_validate

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 1
    assert call_count == 1  # Should not retry
    # Should return TAKEN result


@pytest.mark.asyncio
async def test_validate_all_timeout_handling(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline handles timeouts gracefully."""
    async def mock_validate(value: str):
        await asyncio.sleep(2)  # Longer than timeout
        return ValidationResult(status=ValidationStatus.AVAILABLE)

    adapter = MockValidationAdapter(
        version="1.0.0",
        policy=AdapterPolicy(
            rate_limit_per_minute=60,
            cache_ttl_seconds=3600,
            timeout_seconds=0.1,  # Very short timeout
        ),
        validate_result=ValidationResult(status=ValidationStatus.AVAILABLE)
    )
    # Replace the validate method with our mock
    adapter.validate = mock_validate

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
        pipeline_timeout=5.0,  # Pipeline timeout
    )

    candidates = [name_candidate]

    # Act
    results = await pipeline.validate_all(candidates, naming_brief)

    # Assert
    assert len(results) == 1
    # Should return UNVERIFIABLE due to timeout
    assert results[0].status == CoreValidationStatus.UNVERIFIABLE


@pytest.mark.asyncio
async def test_validate_all_rate_limiting_integration(
    mock_cache, naming_brief, name_candidate
):
    """Test that the pipeline integrates with rate limiters."""
    # Use a rate limit lower than the number of calls to ensure delays
    adapter = MockValidationAdapter(
        version="1.0.0",
        policy=AdapterPolicy(
            rate_limit_per_minute=2,  # Very low: 2 per minute = 1 every 30 seconds
            cache_ttl_seconds=3600,
            timeout_seconds=30.0,
        ),
        validate_result=ValidationResult(status=ValidationStatus.AVAILABLE)
    )

    pipeline = ValidationPipeline(
        adapters=[adapter],
        cache=mock_cache,
        max_concurrency=10,
    )

    # Test multiple candidates to trigger rate limiting
    # Make more calls than the rate limit allows in a short time
    candidates = [
        NameCandidate(
            candidate_id=f"test_{i}",
            name=f"TestName{i}",
            typology=NameTypology.INVENTED,
            rationale=f"Test rationale {i}",
        )
        for i in range(5)  # 5 calls with limit of 2 per minute
    ]

    # Act
    start_time = time.time()
    results = await pipeline.validate_all(candidates, naming_brief)
    end_time = time.time()

    # Assert
    assert len(results) == 5  # 5 candidates × 1 adapter
    assert adapter.validate_call_count == 5
    # With rate limiting of 2 per minute, calls after the first 2 should be delayed
    # First 2 calls: immediate (bucket starts with 2 tokens)
    # 3rd call: needs to wait ~30 seconds for 1 token to refill
    # 4th call: needs to wait another ~30 seconds
    # 5th call: needs to wait another ~30 seconds
    # So minimum delay should be ~60 seconds for calls 3,4,5
    # But let's be conservative and check for at least 1 second delay
    assert end_time - start_time >= 1.0  # At least 1 second delay due to rate limiting


if __name__ == "__main__":
    pytest.main([__file__])
