# ruff: noqa: E501
import urllib.parse

from fastapi.testclient import TestClient

from src.templates.nlp.main import app

client = TestClient(app)

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
        {"entity": "B-PER", "score": 0.99945, "index": 1, "word": "William", "start": 0, "end": 7},
        {"entity": "I-PER", "score": 0.99613, "index": 2, "word": "Henry", "start": 8, "end": 13},
        {"entity": "I-PER", "score": 0.99958, "index": 3, "word": "Gates", "start": 14, "end": 19},
        {"entity": "I-PER", "score": 0.89917, "index": 4, "word": "III", "start": 20, "end": 23},
        {"entity": "B-MISC", "score": 0.99954, "index": 14, "word": "American", "start": 54, "end": 62},
        {"entity": "B-ORG", "score": 0.99871, "index": 34, "word": "Microsoft", "start": 159, "end": 168},
    ]


def test_text_generation_400():
    response = client.get("/text-generation")

    assert response.is_client_error
    assert response.json() == {"detail": "Text must be specified."}


def test_text_generation_200():
    text = "William Henry Gates III (born October 28, 1955) is an"

    response = client.get(f"/text-generation?text={urllib.parse.quote(text)}")

    assert response.is_success
    # don"t blame me :) it's openai-community/gpt2
    assert (
        response.json()["generated_text"]
        == """William Henry Gates III (born October 28, 1955) is an American actor, director, producer, and screenwriter. He is best known for his role as the lead in the 2015 film The Hateful Eight, which was nominated for an Academy Award for Best Actor.\nThe Hateful Eight is a 2015 American film directed by James Cameron. It is based on the novel by the same name by Stephen King. The film was nominated for an Academy Award for Best Picture.\nThe film was released on September"""
    )
