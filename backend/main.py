from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AI Chat Platform")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

class AgentTask(BaseModel):
    task: str
    roles: List[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Chat Platform API"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # Dummy implementation
    return {"response": f"Response from {request.model} to: {request.messages[-1].content}"}

from backend.agents.coordination import DoublendOrchestrator

@app.post("/agents")
def agents_endpoint(task: AgentTask):
    # Initialize Orchestrator for DOUBLEND
    orchestrator = DoublendOrchestrator()

    # Simple logic to assign models to roles based on the requested roles
    for role in task.roles:
        # Defaulting to API type for simplicity in the mock
        # In a real app this would be configured by the user
        model_type = "api"
        model_name = "gpt-3.5-turbo"
        orchestrator.add_agent(role, model_type, model_name)

    results = orchestrator.execute_task(task.task)
    return {"status": "Task executed", "result": results}
