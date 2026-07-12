import datetime
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import (
    Depends,
    FastAPI,
    File,
    HTTPException,
    Query,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.orm import Session

from advanced.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user_by_username,
    verify_password,
)
from advanced.config import settings
from advanced.database import Base, engine, get_db
from advanced.models import Product, User
from advanced.realtime import manager
from advanced.schemas import ProductCreate, ProductResponse, Token, UserCreate, UserResponse

# Upload policy
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_UPLOAD_TYPES = {"image/jpeg", "image/png", "image/gif", "text/plain", "application/pdf"}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Create database tables and the upload directory on startup
    TODO: Replace create_all with Alembic migrations for production
    """
    Base.metadata.create_all(bind=engine)
    Path(settings.upload_dir).mkdir(exist_ok=True)
    yield


app = FastAPI(
    title="Advanced FastAPI Template",
    description="Demonstrates advanced FastAPI features with extensible patterns",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - only the configured origins may call this API from a browser.
# Credentials stay disabled: this API uses Bearer tokens, not cookies.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting setup
# TODO: Replace with Redis for distributed rate limiting in production
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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
    }


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
            status_code=status.HTTP_400_BAD_REQUEST,
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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    User login endpoint (OAuth2 password flow, works with the Swagger UI Authorize button)
    TODO: Add:
    - Account lockout after failed attempts
    - Two-factor authentication
    - Login history tracking
    - Remember me functionality
    """
    user = get_user_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
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
        price=round(product.price * 100),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@app.get("/products/", response_model=list[ProductResponse])
@limiter.limit("30/minute")
async def list_products(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    """
    List products with pagination
    TODO: Add:
    - Filtering by category, price range
    - Sorting options
    - Search functionality
    - Response caching (Redis)
    """
    return (
        db.execute(
            select(Product).offset(skip).limit(limit),
        )
        .scalars()
        .all()
    )


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    """Get product by ID"""
    product = db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


@app.post("/upload/")
@limiter.limit("10/minute")
async def upload_file(
    request: Request,
    file: Annotated[UploadFile, File()],
    current_user: Annotated[User, Depends(get_current_user)],
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
    if file.size and file.size > MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    if file.content_type not in ALLOWED_UPLOAD_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not allowed")

    # Never trust the client-supplied filename: strip any directory components
    safe_name = Path(file.filename or "upload").name
    file_path = Path(settings.upload_dir) / f"{uuid4().hex}_{safe_name}"
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
            await websocket.send_text(f"You wrote: {data}")
            await manager.broadcast(f"Someone wrote: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Someone disconnected")
