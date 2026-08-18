"""Tests for the SocialMediaAdapter."""

from __future__ import annotations

import unittest.mock

import pytest

from launch_engine.validation.adapters.social import SocialMediaAdapter


@pytest.fixture
def social_adapter():
    """Return SocialMediaAdapter instance."""
    return SocialMediaAdapter()


@pytest.mark.asyncio
async def test_social_taken_on_one_platform(social_adapter):
    """Test username taken on at least one platform."""

    # Mock responses: twitter returns 200, instagram returns 404, linkedin returns 404
    def mock_head(url, **kwargs):
        response = unittest.mock.Mock()
        if "twitter.com" in url:
            response.status_code = 200
        elif "instagram.com" in url:
            response.status_code = 404
        elif "linkedin.com" in url:
            response.status_code = 404
        else:
            response.status_code = 404
        return response

    with unittest.mock.patch.object(
        social_adapter._client, "head", side_effect=mock_head
    ):
        result = await social_adapter.validate("exampleuser")

    assert result.status == "taken"
    assert result.social_media == "exampleuser"
    assert result.details is not None
    assert result.details["taken_platforms"] == ["twitter"]
    assert result.details["available_platforms"] == ["instagram", "linkedin"]
    assert result.details["errors"] == []


@pytest.mark.asyncio
async def test_social_available_on_all_platforms(social_adapter):
    """Test username available on all platforms."""

    # Mock responses: all platforms return 404
    def mock_head(url, **kwargs):
        response = unittest.mock.Mock()
        response.status_code = 404
        return response

    with unittest.mock.patch.object(
        social_adapter._client, "head", side_effect=mock_head
    ):
        result = await social_adapter.validate("exampleuser")

    assert result.status == "available"
    assert result.social_media == "exampleuser"
    assert result.details is not None
    assert set(result.details["available_platforms"]) == set(
        [p[0] for p in social_adapter.PLATFORMS]
    )
    assert result.details["taken_platforms"] == []
    assert result.details["errors"] == []


@pytest.mark.asyncio
async def test_social_unverifiable_due_to_error(social_adapter):
    """Test username unverifiable due to error on one platform."""

    # Mock responses: twitter times out, instagram 404, linkedin 404
    def mock_head(url, **kwargs):
        if "twitter.com" in url:
            raise Exception("Timeout")
        elif "instagram.com" in url:
            response = unittest.mock.Mock()
            response.status_code = 404
            return response
        elif "linkedin.com" in url:
            response = unittest.mock.Mock()
            response.status_code = 404
            return response
        else:
            response = unittest.mock.Mock()
            response.status_code = 404
            return response

    with unittest.mock.patch.object(
        social_adapter._client, "head", side_effect=mock_head
    ):
        result = await social_adapter.validate("exampleuser")

    assert result.status == "unverifiable"
    assert result.social_media == "exampleuser"
    assert result.details is not None
    assert result.details["taken_platforms"] == []
    assert result.details["available_platforms"] == ["instagram", "linkedin"]
    assert len(result.details["errors"]) > 0
    assert "twitter" in result.details["errors"][0] or "Timeout" in result.error


@pytest.mark.asyncio
async def test_social_empty(social_adapter):
    """Test empty username."""
    result = await social_adapter.validate("")
    assert result.status == "unverifiable"
    assert result.error == "Empty username"


@pytest.mark.asyncio
async def test_social_adapter_policy(social_adapter):
    """Test that the adapter has the correct policy."""
    assert social_adapter.version == "1.0.0"
    assert social_adapter.policy.rate_limit_per_minute == 30
    assert social_adapter.policy.cache_ttl_seconds == 43200
    assert social_adapter.policy.timeout_seconds == 30.0


@pytest.mark.asyncio
async def test_social_close(social_adapter):
    """Test that we can close the adapter."""
    with unittest.mock.patch.object(
        social_adapter._client, "aclose", return_value=unittest.mock.Mock()
    ) as mock_close:
        await social_adapter.aclose()
        mock_close.assert_called_once()
