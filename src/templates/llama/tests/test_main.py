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
        "How are you today?": "I am doing well, thank you for asking. How about you?",
        "Name the planets in the solar system?": "1. Mercury\n2. Venus\n3. Earth\n4. Mars\n5. Jupiter\n6. Saturn\n7. Uranus\n8. Neptune",
    }

    for question, answer in questions.items():
        response = client.get(f"/question-answering?question={urllib.parse.quote(question)}")

        assert response.is_success
        assert response.json()["answer"] == answer
