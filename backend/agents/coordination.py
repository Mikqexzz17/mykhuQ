from backend.models.api_models import APIPM
from backend.models.local_models import HFPM

class DoublendOrchestrator:
    def __init__(self):
        self.agents = {}

    def add_agent(self, role: str, model_type: str, model_name: str, api_key: str = None):
        if model_type == "api":
            self.agents[role] = APIPM(api_key=api_key or "dummy", model_name=model_name)
        elif model_type == "local":
            self.agents[role] = HFPM(model_id=model_name)
        else:
            raise ValueError("Unknown model type")

    def execute_task(self, task: str) -> dict:
        results = {}
        for role, agent in self.agents.items():
            prompt = f"Role: {role}. Task: {task}"
            results[role] = agent.generate(prompt)
        return results
