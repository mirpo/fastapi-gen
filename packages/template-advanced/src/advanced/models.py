from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from advanced.database import Base


class User(Base):
    """
    User model for authentication
    TODO: Extend with additional fields as needed:
    - profile_picture, bio, last_login
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
    price = Column(Integer)  # stored as integer cents; see ProductResponse.cents_to_dollars
    created_at = Column(DateTime(timezone=True), server_default=func.now())
