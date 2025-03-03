import requests
import re
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user
from app.services.keycloak_service import create_user_keycloak
from app.config import KEYCLOAK_SERVER_URL, KEYCLOAK_REALM

router = APIRouter()

# Initialize the HTTPBearer scheme for authentication
bearer_scheme = HTTPBearer()

@router.post("/user/create", response_model=UserRead)
def create_user_endpoint(
    user_data: UserCreate,
    session: Session = Depends(get_db),  # Dependency to get the database session
    header: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = header.credentials
    print("Received token:", token, type(token))
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
        keycloak_id = create_user_keycloak(
            token, 
            keycloak_payload
        )

        user_data = user_data.dict(exclude={"password"})
        user_data["keycloak_id"] = keycloak_id

        # Proceed to create user in PostgreSQL after Keycloak
        return create_user(session, **user_data)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
