import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.templates.langchain.main import app


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


def test_text_generation_get_missing_param(client):
    """Test text generation endpoint without required parameter"""
    response = client.get("/text-generation")
    assert response.status_code == 422


def test_text_generation_get_success(client):
    """Test text generation with GET method"""
    text = "what is the moon"
    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == text
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data


def test_text_generation_post_success(client):
    """Test text generation with POST method"""
    payload = {"text": "what is the moon"}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == payload["text"]
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data


def test_text_generation_post_with_params(client):
    """Test text generation with custom parameters"""
    payload = {
        "text": "Hello world",
        "max_new_tokens": 50,
        "temperature": 0.5,
    }
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == payload["text"]
    assert "answer" in data
    assert "model_used" in data


def test_question_answering_get_missing_params(client):
    """Test QA endpoint with missing parameters"""
    response = client.get("/question-answering")
    assert response.status_code == 422

    response = client.get("/question-answering?context=some context")
    assert response.status_code == 422


def test_question_answering_get_success(client):
    """Test question answering with GET method"""
    context = "Tom likes coding and designing complex distributed systems."
    question = "What does Tom like?"

    response = client.get(
        f"/question-answering?context={urllib.parse.quote(context)}&question={urllib.parse.quote(question)}",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == context
    assert data["question"] == question
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data


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
    assert "answer" in data
    assert len(data["answer"]) > 0
    assert "model_used" in data


def test_question_answering_post_with_params(client):
    """Test question answering with custom parameters"""
    payload = {
        "context": "The sky is blue during the day.",
        "question": "What color is the sky?",
        "max_new_tokens": 30,
        "temperature": 0.3,
    }
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == payload["context"]
    assert data["question"] == payload["question"]
    assert "answer" in data
    assert "model_used" in data


def test_text_generation_empty_string(client):
    """Test text generation with empty string"""
    payload = {"text": ""}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == ""
    assert "answer" in data


def test_question_answering_empty_context(client):
    """Test QA with empty context"""
    payload = {
        "context": "",
        "question": "What is this about?",
    }
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == ""
    assert data["question"] == payload["question"]
    assert "answer" in data
