import pytest
from fastapi.testclient import TestClient

from llama_app.main import LlamaService, app, settings


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    """Test health check endpoint returns model information"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data
    assert "context_size" in data
    assert "gpu_layers" in data
    assert "threads" in data


def test_question_answering_get_missing_param(client):
    """Test question answering endpoint without required parameter"""
    response = client.get("/question-answering")
    assert response.status_code == 422


def test_question_answering_get_empty_question(client):
    """Test question answering with empty question"""
    response = client.get("/question-answering?question=")
    assert response.status_code == 400
    assert response.json()["detail"] == "Question must be specified."


def test_question_answering_post_success(client):
    """Test question answering with POST method"""
    payload = {"question": "What is machine learning?"}
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == payload["question"]
    assert len(data["answer"]) > 0
    assert data["model_used"] == settings.llm_model
    assert data["tokens_generated"] >= 1


def test_question_answering_post_validation_errors(client):
    """Test POST endpoint validation"""
    # Test empty question
    response = client.post("/question-answering", json={"question": ""})
    assert response.status_code == 422

    # Test invalid max_tokens (too high)
    response = client.post("/question-answering", json={"question": "test", "max_tokens": 5000})
    assert response.status_code == 422

    # Test invalid max_tokens (negative)
    response = client.post("/question-answering", json={"question": "test", "max_tokens": -1})
    assert response.status_code == 422

    # Test invalid temperature (too high)
    response = client.post("/question-answering", json={"question": "test", "temperature": 3.0})
    assert response.status_code == 422

    # Test invalid temperature (negative)
    response = client.post("/question-answering", json={"question": "test", "temperature": -0.1})
    assert response.status_code == 422


def test_question_answering_post_missing_field(client):
    """Test POST endpoint with missing required field"""
    response = client.post("/question-answering", json={})
    assert response.status_code == 422

    # Check that the error mentions the missing field
    errors = response.json()["detail"]
    field_errors = [error for error in errors if error["loc"] == ["body", "question"]]
    assert len(field_errors) > 0
    assert field_errors[0]["type"] == "missing"


def test_generate_answer_honors_zero_temperature():
    """An explicit temperature of 0.0 must not fall back to the configured default"""
    service = LlamaService(settings)
    captured = {}

    def fake_llm(prompt, max_tokens, temperature, echo):
        captured["max_tokens"] = max_tokens
        captured["temperature"] = temperature
        return {"choices": [{"text": "answer"}], "usage": {"completion_tokens": 1}}

    service.llm = fake_llm
    service.generate_answer("test question", max_tokens=None, temperature=0.0)

    assert captured["temperature"] == 0.0
    assert captured["max_tokens"] == settings.llm_max_tokens
