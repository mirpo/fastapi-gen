from fastapi.testclient import TestClient

from src.templates.hello_world.main import app

client = TestClient(app)


def test_root_200():
    response = client.get("/")

    assert response.is_success
    assert response.json() == {"message": "Hello World"}


def test_create_item_200():
    response = client.post(
        "/items/",
        json={"name": "foobar", "description": "the foo bar", "price": "1.23"},
    )

    assert response.is_success
    assert response.json() == {
        "name": "foobar",
        "description": "the foo bar",
        "price": 1.23,
        "tax": None,
    }


def test_create_item_422():
    response = client.post(
        "/items/",
        json={"foo": "bar"},
    )

    assert response.is_client_error
    # or
    assert response.status_code == 422


def test_update_item_200():
    response = client.put(
        "/items/1",
        json={"name": "foobar", "description": "the foo bar", "price": "1.23"},
    )

    assert response.is_success
    assert response.json() == {
        "item_id": 1,
        "name": "foobar",
        "description": "the foo bar",
        "price": 1.23,
        "tax": None,
    }


def test_update_item_422():
    response = client.put(
        "/items/foooobaaaarr",
        json={"name": "foobar", "description": "the foo bar", "price": "1.23"},
    )

    assert response.is_client_error
    # or
    assert response.status_code == 422


def test_read_item200_1():
    response = client.get("/items/1")

    assert response.is_success
    assert response.json() == {"item_id": 1}


def test_read_item200_2():
    response = client.get("/items/1?q=super-query")

    assert response.is_success
    assert response.json() == {"item_id": 1, "q": "super-query"}
