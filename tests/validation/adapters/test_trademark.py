"""Tests for the TrademarkAdapter."""

from __future__ import annotations

import pytest

from launch_engine.validation.adapters.trademark import TrademarkAdapter


@pytest.fixture
def trademark_adapter():
    """Return TrademarkAdapter instance."""
    return TrademarkAdapter()


@pytest.mark.asyncio
async def test_trademark_valid(trademark_adapter):
    """Test trademark validation returns unverifiable with manual review URL."""
    result = await trademark_adapter.validate("ExampleTrademark")

    assert result.status == "unverifiable"
    assert result.trademark == "ExampleTrademark"
    assert result.details is not None
    assert "manual_review_url" in result.details
    assert result.details["manual_review_url"].startswith("https://tmsearch.uspto.gov")


@pytest.mark.asyncio
async def test_trademark_empty(trademark_adapter):
    """Test empty trademark."""
    result = await trademark_adapter.validate("")
    assert result.status == "unverifiable"
    assert result.error == "Empty trademark"


@pytest.mark.asyncio
async def test_trademark_adapter_policy(trademark_adapter):
    """Test that the adapter has the correct policy."""
    assert trademark_adapter.version == "1.0.0"
    assert trademark_adapter.policy.rate_limit_per_minute == 10
    assert trademark_adapter.policy.cache_ttl_seconds == 3600
    assert trademark_adapter.policy.timeout_seconds == 30.0
