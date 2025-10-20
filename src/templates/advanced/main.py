import datetime
import os
from pathlib import Path
from typing import Annotated, Any

from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

# Authentication
import bcrypt
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Database
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.sql import func

app = FastAPI(
    title="Advanced FastAPI Template",
    description="Demonstrates advanced FastAPI features with extensible patterns",
    version="1.0.0",
)

# CORS middleware - Configure for production
# TODO: In production, replace "*" with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting setup
# TODO: Replace with Redis for distributed rate limiting in production
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Database setup - SQLite for simplicity
# TODO: Replace with PostgreSQL for production:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# For async with PostgreSQL: "postgresql+asyncpg://user:password@localhost/dbname"
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """
    User model for authentication
    TODO: Extend with additional fields as needed:
    - profile_picture, bio, created_at, last_login
    - roles table relationship for RBAC
    - email verification status
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Product(Base):
    """
    Sample Product model for CRUD operations
    TODO: Extend with:
    - Categories relationship
    - Inventory tracking
    - Image URLs
    - User ownership (foreign key to User)
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Authentication setup
# TODO: Move SECRET_KEY to environment variables in production
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# In-memory cache - Simple dict for development
# TODO: Replace with Redis for production distributed caching:
# import redis
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
cache: dict[str, Any] = {}


def get_cache_key(prefix: str, *args) -> str:
    """Generate cache key from prefix and arguments"""
    return f"{prefix}:{':'.join(str(arg) for arg in args)}"


def cache_get(key: str) -> Any | None:
    """Get item from cache - Replace with Redis GET in production"""
    return cache.get(key)


def cache_set(key: str, value: Any, expire: int = 300) -> None:
    """Set item in cache - Replace with Redis SETEX in production"""
    # Simple in-memory cache without expiration for demo
    # TODO: Implement TTL with background cleanup or use Redis
    cache[key] = value


class ConnectionManager:
    """
    WebSocket connection manager for real-time features
    TODO: Extend with:
    - Room-based connections (user groups, channels)
    - Message persistence
    - Connection authentication
    - Scaling across multiple servers with Redis pub/sub
    """

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:  # noqa: E722
                self.active_connections.remove(connection)


manager = ConnectionManager()


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt has a 72-byte limit, truncate if necessary
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    # bcrypt has a 72-byte limit, truncate if necessary
    password_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict, expires_delta: datetime.timedelta | None = None):
    """
    Create JWT access token
    TODO: Add refresh token support:
    - Separate refresh token with longer expiry
    - Token revocation list (blacklist)
    - Different permissions in token payload
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Get current authenticated user
    TODO: Add role-based access control:
    - Check user permissions
    - Support for API keys
    - Session management
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.execute(select(User).where(User.username == username)).scalars().first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/")
async def root():
    """Example how use GET and return JSON"""
    return {"message": "Hello World - Advanced Template"}


@app.get("/health")
@limiter.limit("10/minute")  # Rate limiting example
async def health_check(request: Request, db: Annotated[Session, Depends(get_db)]):
    """
    Health check endpoint with timestamp and database connectivity
    TODO: Add checks for:
    - External service dependencies
    - Cache connectivity (Redis)
    - Queue health (Celery/RQ)
    """
    try:
        db.execute(select(1))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.UTC),
        "database": db_status,
        "cache": "healthy" if cache is not None else "unhealthy",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env_dev", ".env.prod"),
    )
    api_version: str = "1.0.0"
    secret_key: str = SECRET_KEY


settings = Settings()
load_dotenv(".env_dev")


def get_settings():
    return settings


@app.get("/version-pydantic-settings")
async def version_pydantic_settings():
    return {"package": "pydantic-settings", "version": settings.api_version}


@app.get("/version-dotenv")
async def version_dotenv():
    return {"package": "dotenv", "version": os.getenv("API_VERSION", "1.0.0")}


@app.get("/config")
async def get_config(settings: Annotated[Settings, Depends(get_settings)]):
    return {"api_version": settings.api_version, "source": "dependency_injection"}


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    tax: float | None = Field(None, ge=0, le=100, description="Tax percentage (0-100)")


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """
    User registration endpoint
    TODO: Add:
    - Email verification
    - Username validation rules
    - Rate limiting for registration attempts
    - CAPTCHA integration
    """
    existing_user = (
        db.execute(
            select(User).where(
                (User.username == user.username) | (User.email == user.email),
            ),
        )
        .scalars()
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered",
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/auth/login", response_model=Token)
@limiter.limit("5/minute")  # Prevent brute force attacks
async def login(
    request: Request,
    username: Annotated[str, Form()] = ...,
    password: Annotated[str, Form()] = ...,
    db: Session = Depends(get_db),
):
    """
    User login endpoint
    TODO: Add:
    - Account lockout after failed attempts
    - Two-factor authentication
    - Login history tracking
    - Remember me functionality
    """
    user = db.execute(select(User).where(User.username == username)).scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """Get current user profile"""
    return current_user


@app.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Create a new product (requires authentication)
    TODO: Add:
    - User ownership of products
    - Category assignment
    - Image upload integration
    - Inventory tracking
    """
    db_product = Product(
        name=product.name,
        description=product.description,
        price=int(product.price * 100),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    response_product = ProductResponse(
        id=db_product.id,
        name=db_product.name,
        description=db_product.description,
        price=db_product.price / 100,
        created_at=db_product.created_at,
    )

    cache_key = get_cache_key("product", db_product.id)
    cache_set(cache_key, response_product.model_dump())

    return response_product


@app.get("/products/", response_model=list[ProductResponse])
@limiter.limit("30/minute")
async def list_products(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List products with pagination and caching
    TODO: Add:
    - Filtering by category, price range
    - Sorting options
    - Search functionality
    - Response compression
    """
    cache_key = get_cache_key("products", skip, limit)
    cached_products = cache_get(cache_key)

    if cached_products:
        return cached_products

    products = (
        db.execute(
            select(Product).offset(skip).limit(limit),
        )
        .scalars()
        .all()
    )

    response_products = [
        ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price / 100,
            created_at=product.created_at,
        )
        for product in products
    ]

    cache_set(cache_key, [p.model_dump() for p in response_products])
    return response_products


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    """Get product by ID with caching"""
    cache_key = get_cache_key("product", product_id)
    cached_product = cache_get(cache_key)

    if cached_product:
        return ProductResponse(**cached_product)

    product = db.execute(select(Product).where(Product.id == product_id)).scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    response_product = ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price / 100,
        created_at=product.created_at,
    )

    cache_set(cache_key, response_product.model_dump())
    return response_product


@app.post("/upload/")
@limiter.limit("10/minute")
async def upload_file(
    request: Request,
    file: Annotated[UploadFile, File()] = ...,
    current_user: User = Depends(get_current_user),
):
    """
    File upload with validation
    TODO: Add:
    - File storage to cloud (S3, GCS)
    - Image processing (resize, compress)
    - Virus scanning
    - User quotas
    - File metadata storage in database
    """
    if file.size and file.size > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    allowed_types = {"image/jpeg", "image/png", "image/gif", "text/plain", "application/pdf"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / f"{datetime.datetime.now().isoformat()}_{file.filename}"
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "path": str(file_path),
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication
    TODO: Add:
    - Authentication for WebSocket connections
    - Room/channel support
    - Message persistence
    - Rate limiting for messages
    - Reconnection handling
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Someone wrote: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Someone disconnected")


def write_log(message: str):
    with open("app.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now(datetime.UTC)}: {message}\n")


@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "notification sent")
    return {"message": "Notification sent in background"}


class CustomError(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError):
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error occurred: {exc.name}"},
    )


@app.get("/error-example")
async def error_example(*, trigger_error: bool = False):
    if trigger_error:
        msg = "example error"
        raise CustomError(msg)
    return {"message": "No error occurred"}


def create_tables():
    """Create database tables on startup"""
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event
    TODO: Add:
    - Database migration checks
    - Cache warming
    - Health check registration
    - Background job initialization
    """
    create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event
    TODO: Add:
    - Graceful connection cleanup
    - Background job termination
    - Cache flush
    - Metrics export
    """
