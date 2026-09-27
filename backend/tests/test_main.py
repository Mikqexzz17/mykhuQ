from fastapi.testclient import TestClient
from backend.main import app
from backend.agents.coordination import DoublendOrchestrator

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Chat Platform API"}

from unittest.mock import patch

@patch('backend.main.APIPM.generate')
def test_chat_endpoint_api(mock_generate):
    mock_generate.return_value = "Mocked API Response"
    response = client.post(
        "/chat",
        json={
            "model": "gpt-3.5-turbo",
            "model_type": "api",
            "api_key": "dummy_key",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    assert response.status_code == 200
    assert response.json()["response"] == "Mocked API Response"

@patch('backend.main.HFPM.generate')
def test_chat_endpoint_local(mock_generate):
    mock_generate.return_value = "Mocked Local Response"
    response = client.post(
        "/chat",
        json={
            "model": "gpt2",
            "model_type": "local",
            "messages": [{"role": "user", "content": "Hello"}]
        }
    )
    assert response.status_code == 200
    assert response.json()["response"] == "Mocked Local Response"

@patch('backend.agents.coordination.APIPM.generate')
@patch('backend.agents.coordination.HFPM.generate')
def test_agents_endpoint(mock_hfpm_generate, mock_apipm_generate):
    mock_apipm_generate.return_value = "Mocked Agent Response"
    response = client.post(
        "/agents",
        json={
            "task": "write code",
            "roles": ["coder", "reviewer"],
            "model_type": "api",
            "model_name": "gpt-3.5-turbo",
            "api_key": "dummy_key"
        }
    )
    assert response.status_code == 200
    results = response.json()["result"]
    assert "coder" in results
    assert "reviewer" in results
    assert "Mocked Agent Response" in results["coder"]
    assert "Mocked Agent Response" in results["reviewer"]

@patch('backend.agents.coordination.APIPM.generate')
@patch('backend.agents.coordination.HFPM.generate')
def test_doublend_orchestrator(mock_hfpm_generate, mock_apipm_generate):
    mock_apipm_generate.return_value = "Mocked APIPM Response"
    mock_hfpm_generate.return_value = "Mocked HFPM Response"

    # We use patch inside the actual implementation so it doesn't trigger HF downloads
    # but we also need to ensure the init logic doesn't crash on download.
    # Because HFPM init downloads the model, we patch HFPM completely for this test.
    with patch('backend.agents.coordination.HFPM') as MockHFPM:
        MockHFPM.return_value.generate.return_value = "Mocked HFPM Response"

        orchestrator = DoublendOrchestrator()
        orchestrator.add_agent("coder", "api", "gpt-4")
        orchestrator.add_agent("reviewer", "local", "dummy-model")

        results = orchestrator.execute_task("test task")
        assert "coder" in results
        assert "reviewer" in results
        assert "Mocked APIPM Response" == results["coder"]
        assert "Mocked HFPM Response" == results["reviewer"]
