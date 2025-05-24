from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.services.keycloak_service import get_token_standard_flow

router = APIRouter()

# Create the login endpoint
@router.post("/login")
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