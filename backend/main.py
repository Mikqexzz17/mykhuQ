from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AI Chat Platform")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    model_type: str # 'api' or 'local'
    api_key: Optional[str] = None
    messages: List[Message]

class AgentTask(BaseModel):
    task: str
    roles: List[str]
    api_key: Optional[str] = None
    model_name: Optional[str] = "gpt-3.5-turbo"
    model_type: Optional[str] = "api"

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Chat Platform API"}

from backend.models.api_models import APIPM
from backend.models.local_models import HFPM

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    prompt = request.messages[-1].content

    if request.model_type == "api":
        if not request.api_key:
            return {"error": "API Key is required for API models"}
        agent = APIPM(api_key=request.api_key, model_name=request.model)
        response = agent.generate(prompt)
    elif request.model_type == "local":
        agent = HFPM(model_id=request.model)
        response = agent.generate(prompt)
    else:
        return {"error": "Invalid model_type. Use 'api' or 'local'."}

    return {"response": response}

from backend.agents.coordination import DoublendOrchestrator

@app.post("/agents")
def agents_endpoint(task: AgentTask):
    if task.model_type == "api" and not task.api_key:
        return {"error": "API Key is required for API models"}

    # Initialize Orchestrator for DOUBLEND
    orchestrator = DoublendOrchestrator()

    # Simple logic to assign models to roles based on the requested roles
    for role in task.roles:
        orchestrator.add_agent(role, task.model_type, task.model_name, task.api_key)

    results = orchestrator.execute_task(task.task)
    return {"status": "Task executed", "result": results}
