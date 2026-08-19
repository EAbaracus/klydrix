"""
Tests for the LLMAdapter class.
"""

from unittest.mock import AsyncMock, patch

import pytest

from litellm.exceptions import APIError
from launch_engine.llm import LLMAdapter


@pytest.mark.parametrize(
    "provider, model, expected_model_id",
    [
        ("ollama", "qwen3:14b", "ollama/qwen3:14b"),
        ("openai", "gpt-3.5-turbo", "openai/gpt-3.5-turbo"),
        ("anthropic", "claude-2", "anthropic/claude-2"),
        ("9router", "some-model", "openai/some-model"),
    ],
)
def test_initialization(provider, model, expected_model_id):
    """Test that the LLMAdapter initializes correctly and sets the model_id."""
    adapter = LLMAdapter(provider=provider, model=model, api_key="test-key")
    assert adapter.provider == provider.lower()
    assert adapter.model == model
    assert adapter.api_key == "test-key"
    assert adapter.model_id == expected_model_id


def test_initialization_unsupported_provider():
    """Test that initializing with an unsupported provider raises a ValueError."""
    with pytest.raises(ValueError):
        LLMAdapter(provider="unsupported", model="some-model")


@pytest.mark.asyncio
async def test_generate_success():
    """Test that generate returns the expected text when the API call succeeds."""
    adapter = LLMAdapter(provider="openai", model="gpt-3.5-turbo", api_key="test-key")

    # Mock the litellm.acompletion function
    mock_response = AsyncMock()
    mock_response.choices = [AsyncMock()]
    mock_response.choices[0].message.content = "Hello, world!"

    with patch("litellm.acompletion", return_value=mock_response) as mock_acompletion:
        result = await adapter.generate("Hello")
        mock_acompletion.assert_called_once()
        # Check that the model string and api_key were passed correctly
        args, kwargs = mock_acompletion.call_args
        assert kwargs["model"] == "openai/gpt-3.5-turbo"
        assert kwargs["api_key"] == "test-key"
        assert kwargs["messages"] == [{"role": "user", "content": "Hello"}]
        assert result == "Hello, world!"


@pytest.mark.asyncio
async def test_generate_llm_api_error():
    """Test that generate raises a RuntimeError when the LLM API call fails."""
    adapter = LLMAdapter(provider="openai", model="gpt-3.5-turbo", api_key="test-key")

    # Mock litellm.acompletion to raise an APIError
    with patch(
        "litellm.acompletion",
        side_effect=APIError(
            status_code=500,
            message="API error",
            llm_provider="openai",
            model="gpt-3.5-turbo",
        ),
    ) as mock_acompletion:
        with pytest.raises(RuntimeError, match="LLM API call failed"):
            await adapter.generate("Hello")
        mock_acompletion.assert_called_once()


@pytest.mark.asyncio
async def test_generate_unexpected_error():
    """Test that generate raises a RuntimeError for unexpected errors."""
    adapter = LLMAdapter(provider="openai", model="gpt-3.5-turbo", api_key="test-key")

    # Mock litellm.acompletion to raise a different exception
    with patch(
        "litellm.acompletion",
        side_effect=ValueError("Unexpected error"),
    ) as mock_acompletion:
        with pytest.raises(RuntimeError, match="Unexpected error during LLM call"):
            await adapter.generate("Hello")
        mock_acompletion.assert_called_once()
