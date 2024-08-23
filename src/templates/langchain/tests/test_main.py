# ruff: noqa: E501
import re
import urllib.parse

from fastapi.testclient import TestClient

from src.templates.langchain.main import app

client = TestClient(app)


def test_text_generation_400():
    response = client.get("/text-generation")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_text_generation_200():
    text = "what is the moon"
    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")


    result = re.sub(r"[^a-zA-Z0-9 ]+", "", response.json()["answer"].strip())
    assert response.is_success
    assert (
        result == "what is the moon    1 100 km2 Moon is 20km3 The moon is about 30050 kilometers4 the Moon has a diameter of 407560 miles5 It is a satellite of the Earth6 it is not a planet7 its orbit is elliptical8 Its orbit has an eccentricity of about9 There is no atmosphere on the surface of11"
    )

def test_question_answering_400():
    response = client.get("/question-answering")

    assert response.is_client_error
    assert response.json() == {"detail": "Context and question must be specified."}


def test_question_answering_200():
    context = "Tom likes coding and designing complex distributed systems."
    question = "What Tom likes?"

    response = client.get(
        f"/question-answering?context={urllib.parse.quote(context)}&question={urllib.parse.quote(question)}",
    )

    result = re.sub(r"[^a-zA-Z0-9 ]+", "", response.json()["answer"].strip())
    assert response.is_success
    assert (
        result
        == "Context Tom likes coding and designing complex distributed systemsQuestion What Tom likesAnswer He likes to code and design complex systems 1 What is the difference between a computer and a machine 200 wordsA computer is a device that can be programmed to perform a task It is an electronic device which can store data process information and execute instructions A machine is any object that performs a specific task and is capable of carrying out a particular task or function Computer and machine are two different things Machine is used to carry out tasks that"
    )
