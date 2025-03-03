from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.services.keycloak_service import get_token

router = APIRouter()

# Create the login endpoint
@router.post("/login")
def login(
    username: str,
    password: str
):
    try:
        token = get_token(
            username=username,
            password=password
        )
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))