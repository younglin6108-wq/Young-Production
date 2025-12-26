"""
Anthropic Claude AI client with cost tracking and model selection.
"""
import os
from typing import Optional
from dataclasses import dataclass
from core.exceptions import AIError, CostLimitExceeded
from utils.cost_tracker import get_cost_tracker, CostTracker


@dataclass
class AIResponse:
    """AI generation response with cost tracking."""
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class AIClient:
    """
    Wrapper around Anthropic Claude API with cost tracking and model selection.
    """

    # Token costs per million tokens (MTok)
    COSTS = {
        "claude-3-5-haiku-20241022": {"input": 0.25, "output": 1.25},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-opus-4-20250514": {"input": 15.00, "output": 75.00}
    }

    def __init__(self, api_key: str, cost_tracker: Optional[CostTracker] = None):
        """
        Initialize AIClient.

        Args:
            api_key: Anthropic API key
            cost_tracker: Optional CostTracker instance (uses singleton if None)
        """
        # Lazy import to avoid dependency if not using AI features
        try:
            import anthropic
            self.anthropic = anthropic
        except ImportError:
            raise ImportError(
                "anthropic package not installed. Run: pip install anthropic"
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_tracker = cost_tracker or get_cost_tracker()

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 1.0
    ) -> AIResponse:
        """
        Generate text using Claude API.

        Args:
            prompt: User prompt
            system: Optional system prompt
            model: Model ID (e.g., "claude-3-5-sonnet-20241022")
            max_tokens: Max output tokens
            temperature: Sampling temperature (0-1)

        Returns:
            AIResponse with generated text and cost

        Raises:
            CostLimitExceeded: If cost limits exceeded before call
            AIError: If API call fails
        """
        # Check cost limits before making call
        self.cost_tracker.check_limits()

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)

            # Calculate cost
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            if model not in self.COSTS:
                # Unknown model - estimate using Sonnet pricing
                print(f"⚠️  Warning: Unknown model {model}, using Sonnet pricing for cost estimate")
                model_costs = self.COSTS["claude-3-5-sonnet-20241022"]
            else:
                model_costs = self.COSTS[model]

            cost_usd = (
                (input_tokens / 1_000_000) * model_costs["input"] +
                (output_tokens / 1_000_000) * model_costs["output"]
            )

            # Extract text
            text = response.content[0].text

            return AIResponse(
                text=text,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd
            )

        except self.anthropic.APIError as e:
            raise AIError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise AIError(f"Unexpected error during AI generation: {str(e)}")

    def generate_with_cost_tracking(
        self,
        prompt: str,
        skill_name: str,
        workflow_name: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate text and automatically track costs.

        Args:
            prompt: User prompt
            skill_name: Skill identifier (e.g., "S05")
            workflow_name: Optional workflow identifier (e.g., "WF1")
            **kwargs: Passed to generate()

        Returns:
            AIResponse

        Raises:
            CostLimitExceeded: If limits exceeded
            AIError: If generation fails
        """
        response = self.generate(prompt, **kwargs)

        # Track cost
        self.cost_tracker.add_cost(
            cost_usd=response.cost_usd,
            skill_name=skill_name,
            workflow_name=workflow_name,
            details={
                "model": response.model,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens
            }
        )

        return response


# Singleton instance
_ai_client_instance: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """
    Get or create AIClient singleton.

    Raises:
        ValueError: If ANTHROPIC_API_KEY not found in environment
    """
    global _ai_client_instance
    if _ai_client_instance is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        _ai_client_instance = AIClient(api_key)
    return _ai_client_instance
