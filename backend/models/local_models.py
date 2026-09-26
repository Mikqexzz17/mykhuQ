class HFPM:
    """Hugging Face Pobranry Model - Represents a model downloaded and run locally."""
    def __init__(self, model_id: str):
        self.model_id = model_id
        # In a real scenario, this would load the model via transformers

    def generate(self, prompt: str) -> str:
        return f"[HFPM {self.model_id}] Simulated local response to: {prompt}"
