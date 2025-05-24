from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.services.keycloak_service import get_token

router = APIRouter()

# Create the auth endpoint
@router.get("/auth")
def auth():
    try:
        token = get_token()
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))