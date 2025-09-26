import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.templates.llama.main import app


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


def test_question_answering_get_success(client):
    """Test question answering with GET method"""
    question = "What is the capital of France?"
    response = client.get(f"/question-answering?question={urllib.parse.quote(question)}")

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == question
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data
    assert "tokens_generated" in data


def test_question_answering_get_with_params(client):
    """Test question answering with GET method and custom parameters"""
    question = "What is Python?"
    max_tokens = 50
    temperature = 0.5

    response = client.get(
        f"/question-answering?question={urllib.parse.quote(question)}&max_tokens={max_tokens}&temperature={temperature}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == question
    assert "answer" in data
    assert "model_used" in data


def test_question_answering_post_success(client):
    """Test question answering with POST method"""
    payload = {"question": "What is machine learning?"}
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == payload["question"]
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data
    assert "tokens_generated" in data


def test_question_answering_post_with_params(client):
    """Test question answering with POST method and custom parameters"""
    payload = {
        "question": "Explain artificial intelligence briefly",
        "max_tokens": 30,
        "temperature": 0.3,
    }
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == payload["question"]
    assert "answer" in data
    assert "model_used" in data
    assert "tokens_generated" in data


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


def test_question_answering_different_questions(client):
    """Test with different types of questions to ensure consistent behavior"""
    questions = [
        "What is 2+2?",
        "Tell me about space exploration",
        "How does photosynthesis work?",
    ]

    for question in questions:
        response = client.post("/question-answering", json={"question": question})
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == question
        assert "answer" in data
        assert len(data["answer"]) > 0
