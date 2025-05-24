import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Base User Schema
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str

# Schema for creating a new user (does not include ID or timestamps)
class UserCreate(UserBase):
    password: str

# Schema for reading (returning) user data
class UserRead(UserBase):
    id: uuid.UUID
    keycloak_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enables ORM compatibility

# Schema for updating a user (optional fields)
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
