from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.services.keycloak_service import (
    get_token, 
    get_token_standard_flow, 
    refresh_access_token, 
    invalidate_token, 
    check_token_validity,
)

router = APIRouter()

# Create the auth endpoint. For test purposes only, this will return a token using client credentials flow.
# Do not expose this endpoint.
@router.get("/auth/token/client")
def auth():
    try:
        token = get_token()
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the login endpoint
@router.post("/auth/login")
def login(
    username: str,
    password: str
):
    try:
        token = get_token_standard_flow(
            username=username,
            password=password
        )
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the refresh token endpoint
@router.post("/auth/token/refresh")
def refresh(refresh_token: str):
    try:
        token = refresh_access_token(refresh_token)
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the logout endpoint
@router.post("/auth/logout")
def logout(refresh_token: str):
    try:
        result = invalidate_token(refresh_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/token/validate")
def validate_token(token: str):
    response = check_token_validity(token)
    try:
        return response
    except ValueError:
        return {"error": response.text, "status_code": response.status_code}