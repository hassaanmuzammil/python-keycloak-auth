from jose import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.keycloak_service import (
    get_token, 
    get_token_standard_flow,
    get_keycloak_public_key, 
    refresh_access_token,
    invalidate_token, 
    check_token_validity,
    reset_password_keycloak,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# Create the auth endpoint. For test purposes only, this will return a token using client credentials flow.
# Do not expose this endpoint.
@router.get("/token/client-credentials")
def get_token_client_credentials():
    try:
        token = get_token()
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the login endpoint
@router.post("/login")
def login(
    username: str,
    password: str,
    session: Session = Depends(get_db)
):
    try:
        token = get_token_standard_flow(
            username=username,
            password=password
        )

        if "access_token" not in token:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Decode JWT to get Keycloak ID (subject)
        public_key = get_keycloak_public_key()
        decoded = jwt.decode(
            token["access_token"], 
            public_key, 
            algorithms=["RS256"], 
            options={"verify_aud": False}
        )
        keycloak_user_id = decoded["sub"]

        # Query DB to validate the user exists and is verified
        user = session.query(User).filter_by(keycloak_id=keycloak_user_id, deleted_at=None).first()

        if not user: 
            raise HTTPException(status_code=403, detail="User does not exist")
        if not user.email_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        return token

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the refresh token endpoint
@router.post("/token/refresh")
def refresh(refresh_token: str):
    try:
        token = refresh_access_token(refresh_token)
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Create the logout endpoint
@router.post("/logout")
def logout(refresh_token: str):
    try:
        result = invalidate_token(refresh_token)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/token/validate")
def validate_token(token: str):
    response = check_token_validity(token)
    try:
        return response
    except ValueError:
        return {"error": response.text, "status_code": response.status_code}


@router.post("/reset-password")
def reset_password(
    user_id: str,
    new_password: str,
    session: Session = Depends(get_db)
):
    try:
        token = get_token()
        # Optional: verify user exists and is not deleted
        user = session.query(User).filter(User.id == user_id, User.deleted_at == None).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        keycloak_user_id = user.keycloak_id
        # Call your existing function to reset the password in Keycloak
        reset_password_keycloak(token["access_token"], keycloak_user_id, new_password)

        return {"message": "Password reset successful"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
