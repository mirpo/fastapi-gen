# ruff: noqa: E501
import os
import urllib.parse

from fastapi.testclient import TestClient

from src.templates.langchain.main import app

client = TestClient(app)
os.environ["TEXT_GENERATION_DO_SAMPLE"] = "False"


def test_text_generation_400():
    response = client.get("/text-generation")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_text_generation_200():
    text = "what is the moon"
    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")

    assert response.is_success
    assert (
        # ruff: disable=E501
        response.json()["answer"]
        == """The moon is a celestial body, and it is not a planet. It is an object of the solar system.
 (The Moon is also called a "planet" because it orbits the sun.)
. The moon has a diameter of about 1.5 million kilometers. (It is about 2.4 million miles.) The diameter is 1,000 kilometers (about 1 million square miles).
, the planet is called the "moon" by the Greek word for "sun.\""""
    )


def test_question_answering_400():
    response = client.get("/question-answering")

    assert response.is_client_error
    assert response.json() == {"detail": "Context and question must be specified."}


def test_question_answering_200():
    context = "Tom likes coding and designing complex distributed systems."
    question = "What Tom likes?"

    response = client.get(
        f"/question-answering?context={urllib.parse.quote(context)}&question={urllib.parse.quote(question)}"
    )

    assert response.is_success
    assert (
        response.json()["answer"]
        == "He likes to write code. He loves to make things. And he likes the idea of having a team of people working on a project. But he also likes being able to do things that are not possible in the real world. So he's a big fan of the open source community. I think that's what he really enjoys."
    )
