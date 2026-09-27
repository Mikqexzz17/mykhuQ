import os
from litellm import completion

class APIPM:
    """API Pobranry Model - Represents a model accessed via external API."""
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # Litellm handles routing to the correct provider (OpenAI, Anthropic, Gemini, etc.)
        # based on the model_name prefix (e.g. "gpt-3.5-turbo", "claude-3-opus", "gemini-pro").
        # We pass the api_key directly to avoid global state mutation and race conditions.

        try:
            response = completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error in APIPM {self.model_name}]: {str(e)}"
