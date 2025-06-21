# ruff: noqa: E501
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient

from src.templates.langchain.main import app, get_langchain_service, LangChainService, Settings

# Mock the LangChain service for testing
@pytest.fixture
def mock_langchain_service():
    mock_service = Mock(spec=LangChainService)
    mock_service.generate_text.return_value = "Mocked text generation result"
    mock_service.answer_question.return_value = "Mocked QA result"
    return mock_service

@pytest.fixture
def client_with_mock(mock_langchain_service):
    app.dependency_overrides[get_langchain_service] = lambda: mock_langchain_service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model" in data
        assert "device" in data

def test_text_generation_get_missing_param():
    with TestClient(app) as client:
        response = client.get("/text-generation")
        assert response.status_code == 422  # Validation error for missing required parameter


def test_text_generation_get_success(client_with_mock):
    text = "what is the moon"
    response = client_with_mock.get(f"/text-generation?text={text}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == text
    assert data["answer"] == "Mocked text generation result"
    assert "model_used" in data

def test_text_generation_post_success(client_with_mock):
    payload = {"text": "what is the moon"}
    response = client_with_mock.post("/text-generation", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == payload["text"]
    assert data["answer"] == "Mocked text generation result"
    assert "model_used" in data

def test_question_answering_get_missing_params():
    with TestClient(app) as client:
        response = client.get("/question-answering")
        assert response.status_code == 422  # Validation error for missing required parameters
        
        response = client.get("/question-answering?context=some context")
        assert response.status_code == 422  # Still missing question parameter


def test_question_answering_get_success(client_with_mock):
    context = "Tom likes coding and designing complex distributed systems."
    question = "What Tom likes?"
    
    response = client_with_mock.get(f"/question-answering?context={context}&question={question}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["context"] == context
    assert data["question"] == question
    assert data["answer"] == "Mocked QA result"
    assert "model_used" in data

def test_question_answering_post_success(client_with_mock):
    payload = {
        "context": "Tom likes coding and designing complex distributed systems.",
        "question": "What Tom likes?"
    }
    response = client_with_mock.post("/question-answering", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["context"] == payload["context"]
    assert data["question"] == payload["question"]
    assert data["answer"] == "Mocked QA result"
    assert "model_used" in data

def test_langchain_service_initialization():
    """Test that LangChainService can be initialized with settings"""
    settings = Settings(text_generation_model="test-model")
    service = LangChainService(settings)
    assert service.settings == settings
    assert service.tokenizer is None
    assert service.model is None
    assert service.pipeline is None
    assert service.llm is None

@patch('src.templates.langchain.main.AutoTokenizer')
@patch('src.templates.langchain.main.AutoModelForCausalLM')
@patch('src.templates.langchain.main.pipeline')
async def test_langchain_service_initialize(mock_pipeline, mock_model, mock_tokenizer):
    """Test LangChainService initialization with mocked dependencies"""
    settings = Settings(text_generation_model="test-model")
    service = LangChainService(settings)
    
    # Mock the components
    mock_tokenizer.from_pretrained.return_value = Mock()
    mock_model.from_pretrained.return_value = Mock()
    mock_model.from_pretrained.return_value.to.return_value = Mock()
    mock_pipeline.return_value = Mock()
    
    await service.initialize()
    
    # Verify initialization was called
    mock_tokenizer.from_pretrained.assert_called_once_with("test-model")
    mock_model.from_pretrained.assert_called_once_with("test-model")
    mock_pipeline.assert_called_once()

def test_settings_device_detection():
    """Test device detection logic in settings"""
    # Test auto detection
    settings = Settings(text_generation_model="test-model", device="auto")
    device = settings.get_device()
    assert device in ["cpu", "cuda"]
    
    # Test explicit device
    settings = Settings(text_generation_model="test-model", device="cpu")
    assert settings.get_device() == "cpu"
