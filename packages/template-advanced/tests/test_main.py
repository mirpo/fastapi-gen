import datetime
from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient

from advanced.main import Base, Settings, app, create_access_token, engine, limiter, settings

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database tables for testing"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_upload_dir():
    """Create the upload directory (done by lifespan in production)"""
    Path(settings.upload_dir).mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Give every test a fresh rate-limit budget"""
    limiter.reset()


def register(username: str, password: str = "password123"):
    """Register a user with a derived email, return the response"""
    return client.post(
        "/auth/register",
        json={"username": username, "email": f"{username}@example.com", "password": password},
    )


@pytest.fixture(scope="module")
def auth_headers():
    """Register and log in a dedicated user, return Authorization headers"""
    assert register("fixtureuser").status_code == 200

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
    response = register("testuser123")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser123"
    assert data["email"] == "testuser123@example.com"
    assert "id" in data
    assert data["is_active"] is True


def test_register_duplicate_user():
    response1 = register("duplicateuser")
    response2 = register("duplicateuser")

    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]


@pytest.mark.parametrize(
    "override",
    [
        {"email": "invalid-email"},
        {"password": "123"},
        {"username": "ab"},
    ],
)
def test_register_invalid_data(override):
    user_data = {
        "username": "validuser",
        "email": "validuser@example.com",
        "password": "password123",
        **override,
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 422


def test_login_flow():
    """Test complete registration -> login -> protected route flow"""
    register_response = register("loginuser", password="loginpassword123")
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


def test_cors_rejects_unknown_origin():
    """Origins outside the configured allowlist get no CORS headers"""
    response = client.get("/", headers={"Origin": "https://evil.example"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_cors_allows_configured_origin():
    """The configured origin is allowed via CORS"""
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_login_rate_limited():
    """Login allows 5 attempts per minute; the 6th is rejected with 429"""
    login_data = {"username": "nonexistentuser12345", "password": "wrongpassword"}
    for _ in range(5):
        response = client.post("/auth/login", data=login_data)
        assert response.status_code == 401
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 429


def test_protected_endpoint_no_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_protected_endpoint_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401


def test_protected_endpoint_expired_token():
    """Expired tokens are rejected with 401"""
    register("expireduser")
    token = create_access_token(
        data={"sub": "expireduser"},
        expires_delta=datetime.timedelta(minutes=-5),
    )
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
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


def test_upload_stores_file_inside_upload_dir(auth_headers):
    """A normal upload lands inside the upload directory with its content intact"""
    response = client.post(
        "/upload/",
        files={"file": ("report.txt", b"hello upload", "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "report.txt"
    assert data["size"] == 12

    stored = Path(data["path"])
    assert stored.read_bytes() == b"hello upload"
    assert stored.resolve().is_relative_to(Path(settings.upload_dir).resolve())


def test_upload_sanitizes_path_traversal_filename(auth_headers):
    """Client filenames with directory components must not escape the upload dir"""
    response = client.post(
        "/upload/",
        files={"file": ("../../evil.txt", b"malicious", "text/plain")},
        headers=auth_headers,
    )
    assert response.status_code == 200

    stored = Path(response.json()["path"])
    assert stored.exists()
    assert stored.resolve().is_relative_to(Path(settings.upload_dir).resolve())


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
    register("secretuser")

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
