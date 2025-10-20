import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.templates.nlp.main import app


@pytest.fixture(scope="session")
def client():
    # Environment variables are set in conftest.py to ensure CPU usage
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    """Test health check endpoint returns model status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "partial"]
    assert "device" in data
    assert "models_loaded" in data
    assert isinstance(data["models_loaded"], dict)


# Summarization tests
def test_summarize_post_success(client):
    """Test summarization with POST method"""
    # Text from https://en.wikipedia.org/wiki/World_map
    text = (
        "A world map is a map of most or all of the surface of Earth. World maps, because of their scale, "
        "must deal with the problem of projection. Maps rendered in two dimensions by necessity distort "
        "the display of the three-dimensional surface of the earth. While this is true of any map, these "
        "distortions reach extremes in a world map. Many techniques have been developed to present world "
        "maps that address diverse technical and aesthetic goals.\n\n"
        "Charting a world map requires global knowledge of the earth, its oceans, and its continents. "
        "From prehistory through the Middle ages, creating an accurate world map would have been impossible "
        "because less than half of Earth's coastlines and only a small fraction of its continental interiors "
        "were known to any culture. With exploration that began during the European Renaissance, knowledge "
        "of the Earth's surface accumulated rapidly, such that most of the world's coastlines had been "
        "mapped, at least roughly, by the mid-1700s and the continental interiors by the twentieth century."
    )
    payload = {"text": text.strip()}
    response = client.post("/summarize", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == text.strip()
    assert "summary_text" in data
    assert len(data["summary_text"]) > 0
    assert "model_used" in data


def test_summarize_post_with_max_length(client):
    """Test summarization with custom max_length"""
    text = "A" * 300  # Create text longer than 200 chars
    payload = {"text": text, "max_length": 50}
    response = client.post("/summarize", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "summary_text" in data


def test_summarize_post_validation_errors(client):
    """Test POST endpoint validation"""
    # Test empty text
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 422

    # Test text too short
    response = client.post("/summarize", json={"text": "short"})
    assert response.status_code == 422

    # Test invalid max_length
    response = client.post("/summarize", json={"text": "A" * 300, "max_length": -1})
    assert response.status_code == 422


def test_summarize_get_success(client):
    """Test summarization with GET method"""
    text = (
        "A world map is a map of most or all of the surface of Earth. World maps, because of their scale, "
        "must deal with the problem of projection. Maps rendered in two dimensions by necessity distort "
        "the display of the three-dimensional surface of the earth. While this is true of any map, these "
        "distortions reach extremes in a world map. Many techniques have been developed to present world "
        "maps that address diverse technical and aesthetic goals.\n\n"
        "Charting a world map requires global knowledge of the earth, its oceans, and its continents. "
        "From prehistory through the Middle ages, creating an accurate world map would have been impossible "
        "because less than half of Earth's coastlines and only a small fraction of its continental interiors "
        "were known to any culture. With exploration that began during the European Renaissance, knowledge "
        "of the Earth's surface accumulated rapidly, such that most of the world's coastlines had been "
        "mapped, at least roughly, by the mid-1700s and the continental interiors by the twentieth century."
    )
    response = client.get(f"/summarize?text={urllib.parse.quote(text)}")

    assert response.status_code == 200
    data = response.json()
    assert "summary_text" in data
    assert "model_used" in data


def test_summarize_get_errors(client):
    """Test GET endpoint error cases"""
    # Test missing text
    response = client.get("/summarize")
    assert response.status_code == 422

    # Test empty text
    response = client.get("/summarize?text=")
    assert response.status_code == 400

    # Test text too short
    response = client.get("/summarize?text=short")
    assert response.status_code == 400


# NER tests
def test_ner_post_success(client):
    """Test NER with POST method"""
    text = (
        "William Henry Gates III (born October 28, 1955) is an American business magnate, investor, "
        "and philanthropist. He is best known for co-founding software giant Microsoft"
    )
    payload = {"text": text}
    response = client.post("/ner", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == text
    assert "entities" in data
    assert isinstance(data["entities"], list)
    assert "model_used" in data


def test_ner_post_validation_error(client):
    """Test NER POST validation"""
    response = client.post("/ner", json={"text": ""})
    assert response.status_code == 422


def test_ner_get_success(client):
    """Test NER with GET method"""
    text = "William Henry Gates III (born October 28, 1955) is an American business magnate"
    response = client.get(f"/ner?text={urllib.parse.quote(text)}")

    assert response.status_code == 200
    entities = response.json()
    assert isinstance(entities, list)


def test_ner_get_error(client):
    """Test NER GET error cases"""
    response = client.get("/ner")
    assert response.status_code == 422

    response = client.get("/ner?text=")
    assert response.status_code == 400


# Text generation tests
def test_text_generation_post_success(client):
    """Test text generation with POST method"""
    payload = {"text": "The future of artificial intelligence is"}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == payload["text"]
    assert "generated_text" in data
    assert len(data["generated_text"]) > len(payload["text"])
    assert "model_used" in data


def test_text_generation_post_with_params(client):
    """Test text generation with custom parameters"""
    payload = {"text": "Hello world", "max_new_tokens": 20, "temperature": 0.5}
    response = client.post("/text-generation", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "generated_text" in data


def test_text_generation_post_validation_errors(client):
    """Test text generation validation"""
    # Test empty text
    response = client.post("/text-generation", json={"text": ""})
    assert response.status_code == 422

    # Test invalid max_new_tokens
    response = client.post("/text-generation", json={"text": "test", "max_new_tokens": -1})
    assert response.status_code == 422

    # Test invalid temperature
    response = client.post("/text-generation", json={"text": "test", "temperature": 3.0})
    assert response.status_code == 422


def test_text_generation_get_success(client):
    """Test text generation with GET method"""
    text = "The weather today is"
    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")

    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == text
    assert "generated_text" in data


def test_text_generation_get_error(client):
    """Test text generation GET error cases"""
    response = client.get("/text-generation")
    assert response.status_code == 422

    response = client.get("/text-generation?text=")
    assert response.status_code == 400


# Question Answering tests
def test_question_answering_post_success(client):
    """Test question answering with POST method"""
    payload = {
        "context": "John is a software engineer who lives in San Francisco. He enjoys hiking and coding.",
        "question": "What does John do for work?",
    }
    response = client.post("/question-answering", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == payload["context"]
    assert data["question"] == payload["question"]
    assert "answer" in data
    assert "confidence" in data
    assert "model_used" in data


def test_question_answering_post_validation_errors(client):
    """Test QA validation"""
    # Test empty context
    response = client.post("/question-answering", json={"context": "", "question": "What?"})
    assert response.status_code == 422

    # Test empty question
    response = client.post("/question-answering", json={"context": "Some context", "question": ""})
    assert response.status_code == 422


def test_question_answering_get_success(client):
    """Test QA with GET method"""
    context = "Python is a programming language"
    question = "What is Python?"
    response = client.get(
        f"/question-answering?context={urllib.parse.quote(context)}&question={urllib.parse.quote(question)}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["context"] == context
    assert data["question"] == question
    assert "answer" in data


def test_question_answering_get_missing_params(client):
    """Test QA GET with missing parameters"""
    response = client.get("/question-answering")
    assert response.status_code == 422

    response = client.get("/question-answering?context=test")
    assert response.status_code == 422


# Embeddings tests
def test_embeddings_success(client):
    """Test embeddings endpoint"""
    payload = {"texts": ["Hello world", "How are you today?"]}
    response = client.post("/embeddings", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["texts"] == payload["texts"]
    assert "embeddings" in data
    assert len(data["embeddings"]) == len(payload["texts"])
    assert "dimension" in data
    assert "model_used" in data


def test_embeddings_validation_error(client):
    """Test embeddings validation"""
    response = client.post("/embeddings", json={"texts": []})
    assert response.status_code == 422


# Sentiment analysis tests
def test_sentiment_success(client):
    """Test sentiment analysis"""
    payload = {"text": "I love this product! It's amazing."}
    response = client.post("/sentiment", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == payload["text"]
    assert "label" in data
    assert "confidence" in data
    assert "model_used" in data


def test_sentiment_validation_error(client):
    """Test sentiment validation"""
    response = client.post("/sentiment", json={"text": ""})
    assert response.status_code == 422


# Zero-shot classification tests
def test_classify_success(client):
    """Test zero-shot classification"""
    payload = {
        "text": "I love programming in Python",
        "candidate_labels": ["technology", "sports", "cooking", "programming"],
    }
    response = client.post("/classify", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == payload["text"]
    assert "labels" in data
    assert "scores" in data
    assert len(data["labels"]) == len(payload["candidate_labels"])
    assert len(data["scores"]) == len(payload["candidate_labels"])
    assert "model_used" in data


def test_classify_validation_errors(client):
    """Test zero-shot classification validation"""
    # Test empty text
    response = client.post("/classify", json={"text": "", "candidate_labels": ["label1", "label2"]})
    assert response.status_code == 422

    # Test empty labels
    response = client.post("/classify", json={"text": "test text", "candidate_labels": []})
    assert response.status_code == 422


# Similarity tests
def test_similarity_success(client):
    """Test text similarity"""
    payload = {"text1": "The cat is sleeping", "text2": "A cat is taking a nap"}
    response = client.post("/similarity", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["text1"] == payload["text1"]
    assert data["text2"] == payload["text2"]
    assert "similarity" in data
    assert isinstance(data["similarity"], float)
    assert "model_used" in data


def test_similarity_validation_errors(client):
    """Test similarity validation"""
    # Test empty text1
    response = client.post("/similarity", json={"text1": "", "text2": "test"})
    assert response.status_code == 422

    # Test empty text2
    response = client.post("/similarity", json={"text1": "test", "text2": ""})
    assert response.status_code == 422


def test_endpoint_error_handling(client):
    """Test that endpoints handle errors gracefully"""
    # All endpoints should return proper error responses
    endpoints_to_test = [
        "/summarize",
        "/ner",
        "/text-generation",
        "/question-answering",
        "/embeddings",
        "/sentiment",
        "/classify",
        "/similarity",
    ]

    for endpoint in endpoints_to_test:
        response = client.post(endpoint, json={})
        assert response.status_code in [400, 422, 500]  # Should not crash
