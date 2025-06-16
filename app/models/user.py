import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

# User model
class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    keycloak_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # roles = relationship(
    #     "Role",
    #     secondary="user_role_link",
    #     back_populates="users"
    # )

class Role(Base):
    __tablename__ = "role"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # users = relationship(
    #     "User",
    #     secondary="user_role_link",
    #     back_populates="roles"
    # )

    capabilities = relationship(
        "Capability",
        secondary="role_capability_link",
        back_populates="roles"
    )

class UserRole(Base):
    __tablename__ = "user_role_link"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Capability(Base):
    __tablename__ = "capability"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    roles = relationship(
        "Role",
        secondary="role_capability_link",
        back_populates="capabilities"
    )

class RoleCapability(Base):
    __tablename__ = "role_capability_link"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    capability_id = Column(UUID(as_uuid=True), ForeignKey("capability.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())