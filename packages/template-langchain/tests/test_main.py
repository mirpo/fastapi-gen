import pytest
from fastapi.testclient import TestClient

import langchain_app.main as main_module
from langchain_app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data
    assert "device" in data


def test_health_reports_unavailable_before_init(monkeypatch):
    """Health must fail when the model service is not initialized"""
    monkeypatch.setattr(main_module, "langchain_service", None)
    plain_client = TestClient(app)

    response = plain_client.get("/health")

    assert response.status_code == 503


def test_text_generation_get_missing_param(client):
    """Test text generation endpoint without required parameter"""
    response = client.get("/text-generation")
    assert response.status_code == 422


def test_text_generation_post_success(client):
    """Test text generation with POST method"""
    payload = {"text": "what is the moon"}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == payload["text"]
    assert len(data["answer"]) > 0
    assert data["model_used"] == main_module.settings.text_generation_model


def test_text_generation_honors_max_new_tokens(client):
    """max_new_tokens in the request must actually limit generation length"""
    text = "Once upon a time"
    response = client.post("/text-generation", json={"text": text, "max_new_tokens": 1})

    assert response.status_code == 200
    answer = response.json()["answer"]
    # The answer echoes the prompt; a single generated token adds only a few characters
    assert len(answer) <= len(text) + 20


def test_question_answering_get_missing_params(client):
    """Test QA endpoint with missing parameters"""
    response = client.get("/question-answering")
    assert response.status_code == 422

    response = client.get("/question-answering?context=some context")
    assert response.status_code == 422


def test_question_answering_post_success(client):
    """Test question answering with POST method"""
    payload = {
        "context": "Tom likes coding and designing complex distributed systems.",
        "question": "What does Tom like?",
    }
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == payload["context"]
    assert data["question"] == payload["question"]
    assert len(data["answer"]) > 0
    assert data["model_used"] == main_module.settings.text_generation_model


def test_text_generation_empty_string(client):
    """Test text generation with empty string"""
    payload = {"text": ""}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == ""
