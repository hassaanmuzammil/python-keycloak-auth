import requests
import re
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import create_user, get_user, update_user, delete_user
from app.services.keycloak_service import (
    get_token, 
    create_user_keycloak, 
    enable_disable_user_keycloak, 
    send_email_verification_link,
)
from app.config import KEYCLOAK_SERVER_URL, KEYCLOAK_REALM

router = APIRouter(prefix="/users", tags=["User"])

# Initialize the HTTPBearer scheme for authentication
bearer_scheme = HTTPBearer()

@router.post("", response_model=UserRead)
async def create_new_user(
    user_data: UserCreate,
    session: Session = Depends(get_db),  # Dependency to get the database session
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    # Use token if you want to validate permissions. 
    # Token belongs to the user making the request. 
    # Check if the user has permission to create a new user.
    # token = header.credentials
    try:
        keycloak_payload = {
            "username": user_data.username,
            "firstName": user_data.first_name,
            "lastName": user_data.last_name,
            "email": user_data.email,
            "enabled": True,
            "credentials": [{"type": "password", "value": user_data.password, "temporary": False}]
        }
        # Now use the token to make the request to Keycloak 
        token = get_token()["access_token"]
        keycloak_user_id = create_user_keycloak(
            token, # token using client credentials, client is authorized to manage users
            keycloak_payload
        )

        user_data = user_data.dict(exclude={"password"})
        user_data["keycloak_id"] = keycloak_user_id

        # Proceed to create user in PostgreSQL after Keycloak
        created_user = create_user(session, **user_data)
        
        # Send email verification link
        send_email_verification_link(token, keycloak_user_id)

        return created_user
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: str,
    session: Session = Depends(get_db),
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = header.credentials  # Validate permissions if needed

    try:
        user = get_user(session, user_id)
        if user:
            return UserRead.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.get("", response_model=list[UserRead])
async def get_all_users(
    session: Session = Depends(get_db),
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    page: int = 1,
    page_size: int = 10,
):
    try:
        query = session.query(User).filter(User.deleted_at == None)
        users = query.offset((page - 1) * page_size).limit(page_size).all()

        # Return empty list if no users found, no 404
        return [UserRead.model_validate(user) for user in users]

    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.put("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_db),
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = header.credentials  # Validate permissions if needed

    try:
        updated_user = update_user(
            session=session,
            user_id=user_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            email_verified=user_data.email_verified,
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))


@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: str,
    session: Session = Depends(get_db),
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = header.credentials  # Validate permissions if needed

    try:
        user = get_user(session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Disable user in Keycloak first
        enable_disable_user_keycloak(
            get_token()["access_token"],
            user.keycloak_id,
            enable=False
        )

        # Now soft delete in users database
        return delete_user(session, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error: " + str(e))