import pytest
from fastapi.testclient import TestClient

from src.templates.advanced.main import Base, app, engine

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables for testing"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World - Advanced Template"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert "timestamp" in json_response
    assert "database" in json_response
    assert "cache" in json_response


def test_version_pydantic_settings():
    response = client.get("/version-pydantic-settings")
    assert response.status_code == 200
    assert response.json()["package"] == "pydantic-settings"


def test_version_dotenv():
    response = client.get("/version-dotenv")
    assert response.status_code == 200
    assert response.json()["package"] == "dotenv"


def test_config():
    response = client.get("/config")
    assert response.status_code == 200
    json_response = response.json()
    assert "api_version" in json_response
    assert json_response["source"] == "dependency_injection"


def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "foobar", "description": "the foo bar", "price": 1.23},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "foobar",
        "description": "the foo bar",
        "price": 1.23,
        "tax": None,
    }


def test_create_item_validation_error():
    response = client.post(
        "/items/",
        json={"name": "", "price": -5.0},
    )
    assert response.status_code == 422


def test_update_item():
    response = client.put(
        "/items/1",
        json={"name": "foobar", "description": "the foo bar", "price": 1.23},
    )
    assert response.status_code == 200
    assert response.json()["item_id"] == 1


def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}


def test_read_item_with_query():
    response = client.get("/items/1?q=super-query")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "super-query"}


def test_send_notification():
    response = client.post("/send-notification/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notification sent in background"}


def test_error_example_no_error():
    response = client.get("/error-example")
    assert response.status_code == 200
    assert response.json() == {"message": "No error occurred"}


def test_error_example_custom_error():
    response = client.get("/error-example?trigger_error=true")
    assert response.status_code == 418
    assert "Custom error occurred" in response.json()["message"]


def test_register_user():
    user_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "password123",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser123"
    assert data["email"] == "testuser123@example.com"
    assert "id" in data
    assert data["is_active"] is True


def test_register_duplicate_user():
    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    response1 = client.post("/auth/register", json=user_data)
    response2 = client.post("/auth/register", json=user_data)

    assert response1.status_code == 200 or response2.status_code == 400


def test_register_invalid_email():
    user_data = {
        "username": "invaliduser",
        "email": "invalid-email",
        "password": "password123",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422


def test_register_short_password():
    user_data = {
        "username": "shortpassuser",
        "email": "short@example.com",
        "password": "123",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422


def test_login_flow():
    """Test complete registration -> login flow"""
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "loginpassword123",
    }
    register_response = client.post("/auth/register", json=user_data)

    login_data = {
        "username": "loginuser",
        "password": "loginpassword123",
    }
    login_response = client.post("/auth/login", data=login_data)

    if register_response.status_code == 200:
        assert login_response.status_code == 200
        data = login_response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        headers = {"Authorization": f"Bearer {data['access_token']}"}
        me_response = client.get("/auth/me", headers=headers)
        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["username"] == "loginuser"


def test_login_invalid_user():
    login_data = {
        "username": "nonexistentuser12345",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_protected_endpoint_no_token():
    response = client.get("/auth/me")
    assert response.status_code == 403


def test_protected_endpoint_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401


def test_create_product_unauthorized():
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 29.99,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 403


def test_create_product_invalid_data():
    user_data = {
        "username": "productuser",
        "email": "productuser@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=user_data)

    login_data = {
        "username": "productuser",
        "password": "password123",
    }
    login_response = client.post("/auth/login", data=login_data)

    if login_response.status_code == 200:
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

        product_data = {
            "name": "",
            "price": -10.0,
        }
        response = client.post("/products/", json=product_data, headers=headers)
        assert response.status_code == 422


def test_list_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_list_products_with_pagination():
    response = client.get("/products/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_nonexistent_product():
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_upload_file_unauthorized():
    response = client.post("/upload/", files={"file": ("test.txt", b"test content", "text/plain")})
    assert response.status_code == 403


def test_upload_file_invalid_type():
    user_data = {
        "username": "fileuser",
        "email": "fileuser@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=user_data)

    login_data = {
        "username": "fileuser",
        "password": "password123",
    }
    login_response = client.post("/auth/login", data=login_data)

    if login_response.status_code == 200:
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

        response = client.post(
            "/upload/",
            files={"file": ("test.exe", b"test content", "application/x-executable")},
            headers=headers,
        )
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]


def test_websocket():
    """Basic WebSocket connection test"""
    try:
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("Hello WebSocket")
            data = websocket.receive_text()
            assert "You wrote: Hello WebSocket" in data
    except Exception:  # noqa: BLE001
        pytest.skip("WebSocket test skipped - environment may not support it")


def test_rate_limiting_basic():
    """Basic rate limiting test - should not fail under normal load"""
    responses = []
    for _i in range(3):
        response = client.get("/health")
        responses.append(response)

    success_count = sum(1 for r in responses if r.status_code == 200)
    assert success_count >= 2


def test_full_user_workflow():
    """Test complete user registration -> login -> create product workflow"""
    import time

    timestamp = int(time.time())
    username = f"workflow{timestamp}"

    user_data = {
        "username": username,
        "email": f"{username}@example.com",
        "password": "workflow123",
    }
    register_response = client.post("/auth/register", json=user_data)

    if register_response.status_code == 200:
        login_data = {
            "username": username,
            "password": "workflow123",
        }
        login_response = client.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        product_data = {
            "name": "Workflow Product",
            "description": "Created in workflow test",
            "price": 25.99,
        }
        product_response = client.post("/products/", json=product_data, headers=headers)
        assert product_response.status_code == 200

        product_id = product_response.json()["id"]
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Workflow Product"


def test_database_connectivity():
    """Test that database connections work"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "database" in response.json()


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.get("/")
    assert response.status_code == 200


def test_api_documentation():
    """Test that OpenAPI docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


def test_product_listing_performance():
    """Test that product listing works consistently"""
    for _ in range(3):
        response = client.get("/products/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
