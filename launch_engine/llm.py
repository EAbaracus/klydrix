"""
LLM Adapter using LiteLLM for provider-agnostic LLM calls.
"""
from typing import Optional
import litellm


class LLMAdapter:
    """
    A provider-agnostic LLM adapter that uses LiteLLM to call various LLM providers.
    """

    def __init__(self, provider: str, model: str, api_key: Optional[str] = None):
        """
        Initialize the LLM adapter.

        Args:
            provider: The LLM provider (ollama, openai, anthropic, 9router).
            model: The model name to use.
            api_key: Optional API key for the provider.
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key

        # Validate provider
        if self.provider not in ["ollama", "openai", "anthropic", "9router"]:
            raise ValueError(f"Unsupported provider: {provider}")

    @property
    def model_id(self) -> str:
        """Full model identifier (e.g., 'ollama/qwen3:14b')."""
        if self.provider == "ollama":
            return f"ollama/{self.model}"
        elif self.provider == "openai":
            return f"openai/{self.model}"
        elif self.provider == "anthropic":
            return f"anthropic/{self.model}"
        elif self.provider == "9router":
            # For 9router, we assume it's an OpenAI-compatible endpoint.
            # We use the model name as-is and rely on environment variables for the base URL.
            return self.model

    async def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM given a prompt.

        Args:
            prompt: The input prompt.

        Returns:
            The generated text response.

        Raises:
            RuntimeError: If the LLM API call fails.
        """
        try:
            response = await litellm.acompletion(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key,
            )
            # Extract the text from the response
            return response.choices[0].message.content
        except litellm.APIError as e:
            raise RuntimeError(f"LLM API call failed: {str(e)}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during LLM call: {str(e)}") from e