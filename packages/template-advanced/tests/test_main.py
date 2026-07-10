import datetime

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from advanced.main import Base, Settings, app, create_access_token, engine, limiter, settings

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables for testing"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def auth_headers():
    """Register and log in a dedicated user, return Authorization headers"""
    user_data = {
        "username": "fixtureuser",
        "email": "fixtureuser@example.com",
        "password": "password123",
    }
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={"username": "fixtureuser", "password": "password123"},
    )
    assert login_response.status_code == 200

    return {"Authorization": f"Bearer {login_response.json()['access_token']}"}


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
    assert json_response["database"] == "healthy"


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

    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


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
    """Test complete registration -> login -> protected route flow"""
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "loginpassword123",
    }
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "loginpassword123"},
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    headers = {"Authorization": f"Bearer {data['access_token']}"}
    me_response = client.get("/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "loginuser"


def test_login_invalid_user():
    login_data = {
        "username": "nonexistentuser12345",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_rate_limited():
    """Login allows 5 attempts per minute; the 6th is rejected with 429"""
    limiter.reset()
    login_data = {"username": "nonexistentuser12345", "password": "wrongpassword"}
    for _ in range(5):
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 401
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 429
    limiter.reset()


def test_protected_endpoint_no_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


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
    assert response.status_code == 401


def test_create_product_invalid_data(auth_headers):
    product_data = {
        "name": "",
        "price": -10.0,
    }
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 422


def test_create_and_get_product(auth_headers):
    """Create a product and fetch it back by id"""
    product_data = {
        "name": "Workflow Product",
        "description": "Created in workflow test",
        "price": 25.99,
    }
    create_response = client.post("/products/", json=product_data, headers=auth_headers)
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["price"] == 25.99

    get_response = client.get(f"/products/{created['id']}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["name"] == "Workflow Product"
    assert fetched["price"] == 25.99


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
    assert response.status_code == 401


def test_upload_file_invalid_type(auth_headers):
    response = client.post(
        "/upload/",
        files={"file": ("test.exe", b"test content", "application/x-executable")},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_websocket():
    """Basic WebSocket connection test"""
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello WebSocket")
        data = websocket.receive_text()
        assert "You wrote: Hello WebSocket" in data


def test_api_documentation():
    """Test that OpenAPI docs are available"""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


def test_secret_key_env_var_overrides_env_file(monkeypatch):
    """SECRET_KEY from the real environment wins over the .env_dev value"""
    monkeypatch.setenv("SECRET_KEY", "env-secret")
    assert Settings().secret_key == "env-secret"


def test_access_token_signed_with_configured_secret(monkeypatch):
    """Tokens must be signed with settings.secret_key so the SECRET_KEY env var takes effect"""
    monkeypatch.setattr(settings, "secret_key", "runtime-configured-secret")
    token = create_access_token(
        data={"sub": "alice"},
        expires_delta=datetime.timedelta(minutes=5),
    )

    payload = jwt.decode(token, "runtime-configured-secret", algorithms=["HS256"])
    assert payload["sub"] == "alice"


def test_auth_me_accepts_token_signed_with_configured_secret(monkeypatch):
    """Token verification must use settings.secret_key, not a hard-coded constant"""
    user_data = {
        "username": "secretuser",
        "email": "secretuser@example.com",
        "password": "password123",
    }
    client.post("/auth/register", json=user_data)

    monkeypatch.setattr(settings, "secret_key", "runtime-configured-secret")
    token = jwt.encode(
        {
            "sub": "secretuser",
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
        },
        "runtime-configured-secret",
        algorithm="HS256",
    )

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
