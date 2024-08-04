# ruff: noqa: E501
import urllib.parse

from fastapi.testclient import TestClient

from src.templates.llama.main import app, settings

client = TestClient(app)
settings.llm_temperature = 0  # disable model randomization to get predictable test results

def test_text_generation_400():
    response = client.get("/question-answering")

    assert response.is_client_error
    assert response.json() == {"detail": "Question must be specified."}


def test_text_generation_200():
    questions = {
        "How are you today?": "I am doing well, thank you for asking! 😊  As an AI, I don't have feelings like humans do, but I'm ready to assist you with any questions or tasks you may have.",
        "What are the Solar System planets in order?": "1. Mercury\n    2. Venus\n    3. Earth\n    4. Mars\n    5. Jupiter\n    6. Saturn\n    7. Uranus\n    8. Neptune\n\n    This is the order of the planets from the Sun outwards.",
    }

    for question, answer in questions.items():
        response = client.get(f"/question-answering?question={urllib.parse.quote(question)}")

        assert response.is_success
        assert response.json()["answer"] == answer
