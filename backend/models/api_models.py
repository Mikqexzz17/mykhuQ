class APIPM:
    """API Pobranry Model - Represents a model accessed via external API."""
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        return f"[APIPM {self.model_name}] Response to: {prompt}"
