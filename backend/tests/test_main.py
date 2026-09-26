from fastapi.testclient import TestClient
from backend.main import app
from backend.agents.coordination import DoublendOrchestrator

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Chat Platform API"}

def test_chat_endpoint():
    response = client.post(
        "/chat",
        json={
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    assert response.status_code == 200
    assert "test-model" in response.json()["response"]
    assert "Hello" in response.json()["response"]

def test_agents_endpoint():
    response = client.post(
        "/agents",
        json={
            "task": "write code",
            "roles": ["coder", "reviewer"]
        }
    )
    assert response.status_code == 200
    results = response.json()["result"]
    assert "coder" in results
    assert "reviewer" in results
    assert "write code" in results["coder"]
    assert "write code" in results["reviewer"]

def test_doublend_orchestrator():
    orchestrator = DoublendOrchestrator()
    orchestrator.add_agent("coder", "api", "gpt-4")
    orchestrator.add_agent("reviewer", "local", "llama-3")

    results = orchestrator.execute_task("test task")
    assert "coder" in results
    assert "reviewer" in results
    assert "[APIPM gpt-4]" in results["coder"]
    assert "[HFPM llama-3]" in results["reviewer"]
