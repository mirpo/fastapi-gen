# ruff: noqa: E501
import urllib.parse

from fastapi.testclient import TestClient

from src.templates.nlp.main import app, settings

client = TestClient(app)
settings.text_generation_do_sample = False  # disable model randomization to get predictable test results


def test_summarize_400_1():
    response = client.get("/summarize")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_summarize_400_2():
    response = client.get("/summarize?text=qwerty")

    assert response.is_client_error
    assert response.json() == {"detail": "Text to summarize is too short. Min length is 200."}


def test_summarize_200():
    # text for the text from https://en.wikipedia.org/wiki/World_map

    text = """
A world map is a map of most or all of the surface of Earth. World maps, because of their scale, must deal with the problem of projection. Maps rendered in two dimensions by necessity distort the display of the three-dimensional surface of the earth. While this is true of any map, these distortions reach extremes in a world map. Many techniques have been developed to present world maps that address diverse technical and aesthetic goals.

Charting a world map requires global knowledge of the earth, its oceans, and its continents. From prehistory through the Middle ages, creating an accurate world map would have been impossible because less than half of Earth's coastlines and only a small fraction of its continental interiors were known to any culture. With exploration that began during the European Renaissance, knowledge of the Earth's surface accumulated rapidly, such that most of the world's coastlines had been mapped, at least roughly, by the mid-1700s and the continental interiors by the twentieth century.
"""
    response = client.get(f"/summarize?text={urllib.parse.quote(text)}")

    assert response.is_success
    assert (
        # ruff: disable=E501
        response.json()["summary_text"]
        == "maps rendered in two dimensions by necessity distort the display of the three-dimensional surface of the earth . this is true of any map, but these distortions reach extremes in a world map . from prehistory through the Middle ages, creating an accurate world map would have been impossible ."
    )


def test_ner_400():
    response = client.get("/ner")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_ner_200():
    # text taken from https://en.wikipedia.org/wiki/Bill_Gates
    text = "William Henry Gates III (born October 28, 1955) is an American business magnate, investor, and philanthropist. He is best known for co-founding software giant Microsoft"

    response = client.get(f"/ner?text={urllib.parse.quote(text)}")

    assert response.is_success
    assert response.json() == [
        {"entity_group": "PER", "score": 0.97358, "word": "William Henry Gates III", "start": 0, "end": 23},
        {"entity_group": "MISC", "score": 0.99954, "word": "American", "start": 54, "end": 62},
        {"entity_group": "ORG", "score": 0.99871, "word": "Microsoft", "start": 159, "end": 168},
    ]


def test_text_generation_400():
    response = client.get("/text-generation")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_text_generation_200():
    text = "William Henry Gates III (born October 28, 1955) is an"

    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")

    assert response.is_success
    # don't blame me :) it's gpt2
    assert (
        response.json()["generated_text"]
        == "William Henry Gates III (born October 28, 1955) is an American actor, writer, and director. He is best known for his role as the character of Dr. Henry Gates in the film The Man Who Fell to Earth. He also appeared in"
    )
