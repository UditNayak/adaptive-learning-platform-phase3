import enum

from sqlalchemy import Column, String, Enum

from app.models.base_entity import BaseEntity


class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseEntity):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole, native_enum=False), nullable=False, default=UserRole.USER)