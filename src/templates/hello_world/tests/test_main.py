from fastapi.testclient import TestClient

from src.templates.hello_world.main import app

client = TestClient(app)


def test_root_200():
    response = client.get("/")

    assert response.is_success
    assert response.json() == {"message": "Hello World"}


def test_health_check_200():
    response = client.get("/health")

    assert response.is_success
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert "timestamp" in json_response


def test_version_pydantic_setting_200():
    response = client.get("/version-pydantic-settings")

    assert response.is_success
    assert response.json() == {"package": "pydantic-settings", "version": "1.0.0"}


def test_version_dotenv_200():
    response = client.get("/version-dotenv")

    assert response.is_success
    assert response.json() == {"package": "dotenv", "version": "1.0.0"}


def test_config_200():
    response = client.get("/config")

    assert response.is_success
    assert response.json() == {"api_version": "1.0.0", "source": "dependency_injection"}


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


def test_create_item_validation_errors():
    # Test empty name
    response = client.post(
        "/items/",
        json={"name": "", "price": 10.0},
    )
    assert response.status_code == 422

    # Test negative price
    response = client.post(
        "/items/",
        json={"name": "test", "price": -5.0},
    )
    assert response.status_code == 422

    # Test invalid tax range
    response = client.post(
        "/items/",
        json={"name": "test", "price": 10.0, "tax": 150.0},
    )
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


def test_send_notification_200():
    response = client.post("/send-notification/")

    assert response.is_success
    assert response.json() == {"message": "Notification sent in background"}


def test_error_example_no_error():
    response = client.get("/error-example")

    assert response.is_success
    assert response.json() == {"message": "No error occurred"}


def test_error_example_custom_error():
    response = client.get("/error-example?trigger_error=true")

    assert response.status_code == 418
    assert response.json() == {"message": "Custom error occurred: example error"}
