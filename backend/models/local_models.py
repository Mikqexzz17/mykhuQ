import threading
from transformers import pipeline

class HFPM:
    """Hugging Face Pobranry Model - Represents a model downloaded and run locally."""
    # We use a dictionary to cache loaded pipelines so we don't reload the model for every request
    _models_cache = {}
    _lock = threading.Lock()

    def __init__(self, model_id: str):
        self.model_id = model_id

        # We load a very small model by default for testing purposes if the user doesn't specify one
        if not self.model_id or self.model_id.strip() == "":
            self.model_id = "gpt2"

        # Load the model if it's not already in the cache
        with self._lock:
            if self.model_id not in self._models_cache:
                print(f"Loading local HF model: {self.model_id}...")
                try:
                    # Using the pipeline for text generation.
                    # In a production environment with large models, you'd use device_map="auto"
                    # and potentially load in 8-bit or 4-bit with accelerate and bitsandbytes.
                    self._models_cache[self.model_id] = pipeline(
                        "text-generation",
                        model=self.model_id,
                        # limit max length to speed up test generations
                        max_new_tokens=50
                    )
                    print(f"Model {self.model_id} loaded successfully.")
                except Exception as e:
                    print(f"Error loading model {self.model_id}: {e}")
                    self._models_cache[self.model_id] = None

    def generate(self, prompt: str) -> str:
        generator = self._models_cache.get(self.model_id)
        if not generator:
            return f"[Error in HFPM] Failed to load or find model {self.model_id}."

        try:
            # Generate text based on the prompt
            result = generator(prompt, return_full_text=False)
            return result[0]['generated_text'].strip()
        except Exception as e:
            return f"[Error in HFPM {self.model_id} generation]: {str(e)}"
